from collections import UserDict
from .contacts_book import Field


class Title(Field):
    """Class representing a name title."""
    pass


class Content(Field):
    """Class representing a name content."""
    pass


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
        """Delete a tag from the note if it exists."""
        if tag in self.tags:
            self.tags.remove(tag)

    def change_content(self, content: str):
        """Change the content of the note."""
        self.content = Content(content) if content else None

    def __str__(self):
        """Return a string representation of the note."""
        tags_str = ", ".join(self.tags) if self.tags else "No tags"
        content_str = self.content if self.content else "No content"
        return f"Title: {self.title.value}, Tags: {tags_str}, \n Content: {content_str.value}"


class NotesBook(UserDict):
    """Class representing a NotesBook."""

    def add_note(self, note: Note):
        """Add a Note to the NotesBook."""
        self.data[note.title.value] = note

    def find(self, title: str):
        """Find a Note by its title."""
        return self.data.get(title, None)

    def delete(self, title: str):
        """Delete a Note from the NotesBook by its title."""
        del self.data[title]

    def __str__(self):
        """Return a string representation of all notes in the NotesBook."""
        notes_str = "\n".join(str(note) for note in self.data.values())
        return f"Notes:\n{notes_str}"
