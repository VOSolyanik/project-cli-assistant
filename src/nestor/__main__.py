import pickle
from typing import List, Tuple

from handlers.contacts import ContactsHandler
from handlers.notes import NotesHandler
from services.colorizer import Colorizer
from models.contacts_book import ContactsBook
from models.notes_book import NotesBook

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def load_data(filename="contacts_book.pkl"):
    """
    Loads data from file, returns empty contacts book if file not found
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # Return empty contacts book if file not found
        return ContactsBook()

def save_data(book, filename="contacts_book.pkl"):
    """
    Saves data to file
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def main():
    # load ContactsBook and initialize contacts handler
    contacts_book = load_data()
    contacts_handler = ContactsHandler(contacts_book)
    notes_handler = NotesHandler(NotesBook())

    print(Colorizer.highlight("Welcome to the assistant bot!"))
    while True:
        user_input = ""
        try:
            user_input = input(Colorizer.info("Enter a command: "))
        # handle Exit on Ctrl+C
        except KeyboardInterrupt:
            print(Colorizer.highlight("\nGood bye!"))
            save_data(contacts_book)
            break

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(Colorizer.highlight("Good bye!"))
            save_data(contacts_book)
            break
        elif command == "hello":
            print(Colorizer.highlight("How can I help you?"))
        elif command == "help":
            #todo: Implement
            pass
        elif command in ContactsHandler.get_available_commands():
            print(contacts_handler.handle(command, *args))
        elif command in NotesHandler.get_available_commands():
            print(notes_handler.handle(command, *args))
        else:
            print(Colorizer.error("Invalid command."))

if __name__ == "__main__":
    main()
