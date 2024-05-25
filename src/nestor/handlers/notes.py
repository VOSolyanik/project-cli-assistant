from nestor.handlers.base import CommandsHandler
from nestor.handlers.command_data_collector import FieldInput, command_data_collector
from nestor.models.notes_book import Content, NotesBook, Note, Title
from nestor.services.ui import UserInterface
from nestor.services.colorizer import Colorizer
from nestor.utils.input_error import input_error
from nestor.utils.csv_as_table import csv_as_table
from nestor.utils.to_csv import to_csv

class NotesHandler(CommandsHandler):
    """
    Notes handler class
    book: NotesBook - notes book instance
    """

    NOTES_COMMAND = "notes"
    ADD_NOTE = "add-note"
    DELETE_NOTE = "delete-note"
    EDIT_NOTE = "edit-note"
    ADD_NOTE_TAGS = "add-note-tags"
    DELETE_NOTE_TAGS = "delete-note-tags"
    SEARCH_NOTES = "search-notes"

    def __init__(self, book: NotesBook, cli: UserInterface):
        self.book = book
        self.cli = cli


    @staticmethod
    def get_available_commands() -> list[str]:
        """
        Returns list of available commands
        """
        return [
            NotesHandler.NOTES_COMMAND,
            NotesHandler.ADD_NOTE,
            NotesHandler.EDIT_NOTE,
            NotesHandler.DELETE_NOTE,
            NotesHandler.SEARCH_NOTES,
            NotesHandler.ADD_NOTE_TAGS,
            NotesHandler.DELETE_NOTE_TAGS
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
            case NotesHandler.EDIT_NOTE:
                return self.__edit_note(*args)
            case NotesHandler.DELETE_NOTE:
                return self.__delete_note(*args)
            case NotesHandler.NOTES_COMMAND:
                return self.__get_all_notes()
            case NotesHandler.SEARCH_NOTES:
                return self.__search_notes(*args)
            case NotesHandler.ADD_NOTE_TAGS:
                return self.__add_note_tags(*args)
            case NotesHandler.DELETE_NOTE_TAGS:
                return self.__delete_note_tags(*args)
            case _:
                return Colorizer.error("Invalid command.")

    @input_error({KeyboardInterrupt: "Note adding interrupted. Note not added."})
    def __add_note(self) -> str:
        """
        Adds note to notebook dictionary
        """
        fields = [
            FieldInput(prompt="Title", validator=Title.validate, is_required=True),
            FieldInput(prompt="Content", validator=Content.validate, is_required=True),
            FieldInput(prompt="Tags (separated by semicolon)"),
        ]

        title, content, tags_str = command_data_collector(fields, self.cli)
        tags = self.__tags_from_str(tags_str)

        note = self.book.find(title)

        if note is None:
            note = Note(title, content, tags)
            self.book.add(note)
            message = Colorizer.success(f"Note \"{title}\" added.")
        else:
            message = Colorizer.warn(f"Note \"{title}\" already exist.")

        return message

    @input_error({KeyboardInterrupt: "Note editing interrupted. Note not updated.", IndexError: "Note title is required"})
    def __edit_note(self, *args) -> str:
        """
        Edit note in notebook dictionary
        """
        title = args[0]
        record = self.book.find(title)

        if record is None:
            message = Colorizer.warn(f"Could not find Note \"{title}\".")
        else:
            fields = [
                FieldInput(prompt="Title", default_value=record.title, validator=Title.validate, is_required=True),
                FieldInput(prompt="Content", default_value=record.content, validator=Content.validate, is_required=True),
                FieldInput(prompt="Tags (separated by semicolon)", default_value="; ".join(record.tags) if record.tags else ""),
            ]
            new_title, content, tags_str = command_data_collector(fields, self.cli)
            tags = self.__tags_from_str(tags_str)

            if new_title and new_title != record.title.value and self.book.find(new_title):
                return Colorizer.warn(f"Note with title '{new_title}' already exist.")
            elif new_title and new_title != record.title.value:
                record.edit_title(new_title)
                self.book.delete(title)
                self.book.add(record)

            if content:
                record.edit_content(content)
            if tags:
                record.edit_tags(tags)

            message = Colorizer.success(f"Content for Note \"{title}\" was changed.")

        return message


    @input_error({IndexError: "Note title is required"})
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
        Searches notes by title, content and tags
        """
        search_str = args[0]
        notes = self.book.search(search_str)

        if not notes:
            return Colorizer.warn("No notes found")

        return csv_as_table(to_csv(notes))


    @input_error({ValueError: "Note title and tags are required"})
    def __add_note_tags(self, *args) -> str:
        """
        Adds tags to note in notebook dictionary
        """

        title, tags_str = args
        tags = self.__tags_from_str(tags_str)
        note = self.book.find(title)

        if note is None:
            message = Colorizer.warn(f"Could not find Note \"{title}\".")
        else:
            note.add_tags(tags)
            message = Colorizer.success(f"Tags added for Note \"{title}\".")

        return message


    @input_error({IndexError: "Note title is required"})
    def __delete_note_tags(self, *args) -> str:
        """
        Remove tags from note in notebook dictionary
        """
        title = args[0]
        note = self.book.find(title)

        if note is None:
            message = Colorizer.warn(f"Could not find Note \"{title}\".")
        else:
            note.delete_tags()
            message = Colorizer.success(f"Tags deleted for Note \"{title}\".")

        return message


    @input_error()
    def __get_all_notes(self) -> str:
        if not self.book.data:
            return Colorizer.warn("Notes not found")

        return csv_as_table(to_csv(list(self.book.data.values())))
    
    def __tags_from_str(self, tags_str: str | None) -> list[str]:
        """
        Converts tags string to list of tags
        tags_str: str - tags string
        """
        if not tags_str:
            return []
        
        tags = map(lambda x: x.strip(), tags_str.split(";")) if tags_str else []
        return list(filter(lambda x: x, tags))
