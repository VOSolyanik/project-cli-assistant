from collections import UserDict
from nestor.models.contacts_book import Field
from nestor.models.exceptions import TitleValueError, ContentValueError


class Title(Field):
    """Class representing a name title."""

    MAX_TITLE_LENGTH = 20

    @staticmethod
    def validate(value: str) -> None:
        if value is None or len(value) == 0:
            raise TitleValueError("Title is required")
        if value is None or len(value) > Title.MAX_TITLE_LENGTH:
            raise TitleValueError(f"Title should be less then {Title.MAX_TITLE_LENGTH} symbols")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        Title.validate(value)

        self._value = value


class Content(Field):
    """Class representing a name content."""

    MAX_CONTENT_LENGTH = 200

    @staticmethod
    def validate(value: str) -> None:
        if value is None or len(value) > Content.MAX_CONTENT_LENGTH:
            raise ContentValueError(f"Content should be less then {Content.MAX_CONTENT_LENGTH} symbols")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        Content.validate(value)

        self._value = value

        
class Note:
    """Class representing a record for NotesBook."""

    def __init__(self, title, content=None, tags=None):
        """Initialize a new Note."""
        self.title = Title(title)
        self.tags = tags if tags else []  # Initialize tags
        self.content = Content(content) if content else None  # Initialize note content

    def add_tag(self, tag: str):
        """Add a new tag to the note if it does not already exist."""
        if tag not in self.tags:
            self.tags.append(tag)

    def delete_tag(self, tag: str):
        """Delete a tag for the note if it exists."""
        if tag in self.tags:
            self.tags.remove(tag)

    def edit_content(self, content: str):
        """Change the content of the note."""
        self.content = Content(content) if content else None

    def edit_title(self, title: str):
        """Change the title of the note."""
        self.title = Title(title) if title else None

    def edit_tags(self, tags: list[str]):
        """Edit a tags for the note if it exists."""
        self.tags = tags if tags else []

    def __str__(self):
        """Return a string representation of the note."""

        tags_str = ", ".join(self.tags) if self.tags else "No tags"
        content_str = self.content if self.content else "No content"
        return f"Title: {self.title}, Tags: {tags_str}, \n Content: {content_str}"


class NotesBook(UserDict):
    """Class representing a NotesBook."""

    def add(self, note: Note):
        """Add a Note to the NotesBook."""
        self.data[note.title.value] = note

    def find(self, title: str) -> Note | None:
        """Find a Note by its title."""
        return self.data.get(title, None)

    def delete(self, title: str):
        """Delete a Note from the NotesBook by its title."""
        del self.data[title]

    def search(self, search_str: str) -> list[Note]:
        """Search records by title and content."""

        result = []
        for record in self.data.values():
            if (search_str.lower() in str(record.title).lower() or
                (search_str.lower() in str(record.content).lower())):
                result.append(record)
        return result


    def __str__(self):
        """Return a string representation of all notes in the NotesBook."""
        notes_str = "\n".join(str(note) for note in self.data.values())
        return f"Notes:\n{notes_str}"
