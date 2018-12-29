from django.core.management import get_commands
from django.http import HttpResponse
from django.shortcuts import render


def commands_list(request):
    commands = get_commands()
    commands_list = [ {'command': key, 'module': value} for key, value in commands.items()]

    return render(request, 'command_list.html', {
        'commands': commands_list,
    })