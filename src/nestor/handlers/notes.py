from models.notes_book import NotesBook, Note
from utils.input_error import input_error
from services.colorizer import Colorizer

class NotesHandler():
    """
    Notes handler class
    book: NotesBook - notes book instance
    """

    NOTES_COMMAND = "all-notes"
    ADD_NOTE = "add-note"
    DELETE_NOTE = "delete-note"
    CHANGE_NOTE = "change-note"

    def __init__(self, book: NotesBook):
        self.book = book


    @staticmethod
    def get_available_commands() -> list[str]:
        """
        Returns list of available commands
        """
        return [
            NotesHandler.NOTES_COMMAND,
            NotesHandler.DELETE_NOTE,
            NotesHandler.ADD_NOTE,
            NotesHandler.CHANGE_NOTE,

        ]
    
    def help(self, command=None):
        commands = {
            self.NOTES_COMMAND: "Show all notes. Example: all-notes",
            self.ADD_NOTE: "Add a note. Example: add-note <title> <content>",
            self.DELETE_NOTE: "Delete a note. Example: delete-note <title>",
            self.CHANGE_NOTE: "Change a note. Example: change-note <title> <new content>"
        }

        if command:
            if command in commands:
                help_message = f"{command}: {commands[command]}\n"
            else:
                help_message = f"No help available for {command}\n"
        else:
            help_message = "Available commands:\n"
            for cmd, description in commands.items():
                help_message += f"{cmd}: {description}\n"

        return help_message

    def handle(self, command: str, *args: list[str]) -> str:
        """
        Handles user commands
        command: str - user command
        args: list[str] - command arguments
        """
        match command:
            case NotesHandler.ADD_NOTE:
                return self.__add_note(*args)
            case NotesHandler.CHANGE_NOTE:
                return self.__change_note(*args)
            case NotesHandler.DELETE_NOTE:
                return self.__delete_note(*args)
            case NotesHandler.NOTES_COMMAND:
                return self.__get_all_notes()
            case _:
                return Colorizer.error("Invalid command.")

    @input_error()
    def __add_note(self, *args) -> str:
        """
        Adds note to notebook dictionary
        """
        title, content = args
        note = self.book.find(title)

        if note is None:
            note = Note(title, content)
            self.book.add_note(note)
            message = Colorizer.success(f"Note \"{title}\" added.")
        else:
            message = Colorizer.warn(f"Note \"{title}\" already exist.")

        return message

    @input_error()
    def __change_note(self, *args) -> str:
        """
        Change (replace content) for note by given title
        """
        title, content = args
        record = self.book.find(title)

        if record is None:
            message = Colorizer.warn(f"Could not find Note \"{title}\".")
        else:
            record.change_content(content)
            message = Colorizer.success(f"Content for Note \"{title}\" was changed.")

        return message

    @input_error()
    def __delete_note(self, *args) -> str:
        title = args[0]
        record = self.book.find(title)

        if record is None:
            message = Colorizer.warn(f"Could not find Note \"{title}\".")
        else:
            self.book.delete(title)
            message = Colorizer.warn(f"Note \"{title}\" deleted.")

        return message

    @input_error()
    def __get_all_notes(self, *args) -> str:
        if not self.book.data:
            return Colorizer.warn("Notes not found")

        return Colorizer.highlight("\n".join([str(record) for record in self.book.data.values()]))
