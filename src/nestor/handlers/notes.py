from models.notes_book import NotesBook, Note
from utils.input_error import input_error
from services.colorizer import Colorizer
from nestor.utils.to_csv import to_csv
from nestor.utils.csv_as_table import csv_as_table

class NotesHandler():
    """
    Notes handler class
    book: NotesBook - notes book instance
    """

    NOTES_COMMAND = "notes"
    ADD_NOTE = "add-note"
    DELETE_NOTE = "delete-note"
    CHANGE_NOTE = "change-note"
    SEARCH_NOTES = "search-note"

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
            NotesHandler.SEARCH_NOTES
        ]

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
            case NotesHandler.SEARCH_NOTES:
                return self.__search_notes(*args)
            case _:
                return Colorizer.error("Invalid command.")

    @input_error({ValueError: "Note title and content are required"})
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

    @input_error({ValueError: "Note title and content are required"})
    def __change_note(self, *args) -> str:
        """
        Change (replace) content for note by given title
        """
        title, content = args
        record = self.book.find(title)

        if record is None:
            message = Colorizer.warn(f"Could not find Note \"{title}\".")
        else:
            record.change_content(content)
            message = Colorizer.success(f"Content for Note \"{title}\" was changed.")

        return message

    @input_error({ValueError: "Note title are required"})
    def __delete_note(self, *args) -> str:
        title = args[0]
        record = self.book.find(title)

        if record is None:
            message = Colorizer.warn(f"Could not find Note \"{title}\".")
        else:
            self.book.delete(title)
            message = Colorizer.warn(f"Note \"{title}\" deleted.")

        return message
    
    @input_error({IndexError: "Search string is required"})
    def __search_notes(self, *args) -> str:
        """
        Searches notes by title, content
        args: list[str] - command arguments
        """
        search_str = args[0]
        notes = self.book.search(search_str)
        
        if not notes:
            return Colorizer.warn("No notes found")
        
        return csv_as_table(to_csv(notes))

    @input_error()
    def __get_all_notes(self, *args) -> str:
        if not self.book.data:
            return Colorizer.warn("Notes not found")

        return csv_as_table(to_csv(list(self.book.data.values())))
