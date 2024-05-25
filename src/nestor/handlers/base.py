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
    
    def help(self) -> str:
        """ Returns help message """
        pass