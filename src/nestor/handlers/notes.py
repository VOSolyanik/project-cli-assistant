from models.notes_book import NotesBook

class NotesHandler():
    """
    Notes handler class
    book: NotesBook - notes book instance
    """
    def __init__(self, book: NotesBook):
        self.book = book

    @staticmethod
    def get_available_commands() -> list[str]:
        """
        Returns list of available commands
        """
        return []

    def handle(self, command: str, *args: list[str]) -> str:
        """
        Handles user commands
        command: str - user command
        args: list[str] - command arguments
        """
        pass
    