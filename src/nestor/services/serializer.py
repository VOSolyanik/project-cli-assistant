import pickle

from nestor.models.contacts_book import ContactsBook
from nestor.models.notes_book import NotesBook


class Storage:
    """
    Storage class for contacts book and notes book.
    """
    def __init__(self):
        self.contacts_book = ContactsBook()
        self.notes_book = NotesBook()


class Serializer:
    """
    Serializer class for loading and saving data.
    """
    def __init__(self, filename):
        self.filename = f"{filename}.pkl"

    def load_data(self) -> Storage:
        """
        Loads data from file, returns empty contacts book if file not found.
        """
        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            # Return empty contacts book if file not found
            return Storage()

    def save_data(self, storage: Storage):
        """
        Saves data to file.
        """
        with open(self.filename, "wb") as f:
            pickle.dump(storage, f)