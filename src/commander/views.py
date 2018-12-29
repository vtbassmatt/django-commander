from io import StringIO

from django.core.management import (
    get_commands,
    load_command_class,
    call_command,
    CommandError)
from django.http import HttpResponse, Http404
from django.shortcuts import render

from .forms import CommandForm


COMMAND_BLACKLIST = (
    ('shell', 'django.core'),
    ('dbshell', 'django.core'),
    ('runserver', 'django.core'),
    ('testserver', 'django.core'),
)


def get_filtered_commands():
    commands = get_commands()
    for filter_command, filter_module in COMMAND_BLACKLIST:
        if filter_command in commands and commands[filter_command] == filter_module:
            del commands[filter_command]
    return commands


def command_list(request):
    commands = get_filtered_commands()
    commands_list = [ {'command': key, 'module': value} for key, value in commands.items()]

    return render(request, 'command_list.html', {
        'commands': commands_list,
    })


def command_run(request, name):
    commands = get_filtered_commands()
    if not name in commands:
        raise Http404(name)

    cmd = load_command_class(commands[name], name)
    parser = cmd.create_parser('manage.py', name)

    response_context = {
        'command_name': name,
        'command_usage': parser.format_help(),
    }

    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            args = form.cleaned_data['args'].split()
            stdout = StringIO()
            try:
                ret_val = call_command(cmd, stdout=stdout, stderr=stdout, *args)
                response_context['command_results'] = "\n".join([
                    f"Return value: {ret_val or None}",
                    "-------",
                    stdout.getvalue(),
                ])
            except CommandError as exc:
                response_context['command_results'] = str(exc)
            except SystemExit:
                pass
            stdout.close()
    else:
        form = CommandForm()

    form.fields['args'].label = name
    response_context['form'] = form

    return render(request, 'command_details.html', response_context)
