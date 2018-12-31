from io import StringIO

from django.core.exceptions import ImproperlyConfigured
from django.core.management import (
    load_command_class,
    call_command,
    CommandError)
from django.http import HttpResponse, Http404
from django.shortcuts import render

from .commands import get_filtered_commands
from .forms import CommandForm
from .protection import protect_with_key


@protect_with_key
def command_list(request):
    commands = get_filtered_commands()
    commands_list = [ {'command': key, 'module': value} for key, value in commands.items()]

    return render(request, 'command_list.html', {
        'commands': commands_list,
        'key': request.GET['key'],
    })


@protect_with_key
def command_run(request, name):
    commands = get_filtered_commands()
    if not name in commands:
        raise Http404(name)

    cmd = load_command_class(commands[name], name)
    parser = cmd.create_parser('manage.py', name)

    response_context = {
        'command_name': name,
        'command_usage': parser.format_help(),
        'key': request.GET['key'],
    }

    has_noinput = True if '--noinput' in response_context['command_usage'] else False

    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            args = form.cleaned_data['args'].split()
            if has_noinput and form.cleaned_data['automatic_noinput']:
                args.append('--noinput')
            stdout = StringIO()
            try:
                ret_val = call_command(cmd, stdout=stdout, stderr=stdout, *args)
                response_context['command_results'] = "\n".join([
                    f"Return value: {ret_val or None}",
                    "-------",
                    stdout.getvalue(),
                ])
            except (CommandError, ImproperlyConfigured) as exc:
                response_context['command_results'] = "\n".join([
                    'Exception: ' + exc.__class__.__name__,
                    str(exc),
                ])
            except SystemExit:
                pass
            stdout.close()
    else:
        form = CommandForm()

    form.fields['args'].label = name
    response_context['form'] = form

    return render(request, 'command_details.html', response_context)
