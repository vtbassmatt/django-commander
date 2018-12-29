from io import StringIO

from django.core.management import get_commands, load_command_class
from django.http import HttpResponse, Http404
from django.shortcuts import render


def command_list(request):
    commands = get_commands()
    commands_list = [ {'command': key, 'module': value} for key, value in commands.items()]

    return render(request, 'command_list.html', {
        'commands': commands_list,
    })

def command_run(request, name):
    commands = get_commands()
    if not name in commands:
        raise Http404(name)

    cmd = load_command_class(commands[name], name)
    parser = cmd.create_parser('manage.py', name)
    return render(request, 'command_details.html', {
        'command_usage': parser.format_help(),
    })
