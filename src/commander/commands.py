from django.core.management import get_commands


COMMAND_BLACKLIST = (
    ('shell', 'django.core'),
    ('dbshell', 'django.core'),
    ('runserver', 'django.contrib.staticfiles'),
    ('testserver', 'django.core'),
)


def get_filtered_commands():
    commands = get_commands()
    for filter_command, filter_module in COMMAND_BLACKLIST:
        if filter_command in commands and commands[filter_command] == filter_module:
            del commands[filter_command]
    return commands
