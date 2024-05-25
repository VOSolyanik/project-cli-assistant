from typing import Dict

from nestor.services.colorizer import Colorizer


class CommandsHandler():
    """ Base class for handling commands """
    @staticmethod
    def get_available_commands() -> list[str]:
        """
        Returns list of available commands
        """
        return [ ]

    def handle(self, command: str, *args: list[str]) -> str:
        """ Handles user commands """
        pass
    
    def help(self, command) -> str:
        """ Returns help message """
        pass

    def _get_help_message(self, commands: Dict[str, str], title: str, command: str = None) -> str:
        """ Returns info of available commands """
        if command:
            if command in commands:
                help_message = f"{Colorizer.highlight(command)}: {Colorizer.info(commands[command])}\n"
            else:
                help_message = Colorizer.warn(f"No help available for {command}\n")
        else:
            help_message = Colorizer.info(title + "\n\n")
            for cmd, description in commands.items():
                help_message += f"{Colorizer.highlight(cmd)}: {Colorizer.info(description)}\n\n"

        return help_message