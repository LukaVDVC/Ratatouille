class CommandHelp:
    COMMANDS = {
        'help': 'Display this help message.',
        'download <filepath>': 'Download a file from the victim to the server.',
        'upload <filepath> <destination>': 'Upload a file from the server to the victim.',
        'shell <command>': 'Open an interactive shell (bash or cmd).',
        'ipconfig': 'Obtain the network configuration of the victim machine.',
        'screenshot': 'Take a screenshot of the victim machine.',
        'search <filename>': 'Search for a file on the victim machine.',
        'hashdump': 'Retrieve the SAM database or the shadow file of the machine.',
        'sysinfo': 'Get system information of the victim machine.',
        'exit': 'Exit the RAT.',
        'quit': 'Quit the RAT.'
    }

    @staticmethod
    def get_help():
        help_message = "Available Commands:\n"
        for command, description in CommandHelp.COMMANDS.items():
            help_message += f"{command}: {description}\n"
        return help_message
