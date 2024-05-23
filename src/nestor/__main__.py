import shlex
from typing import List, Tuple

from nestor.handlers.contacts import ContactsHandler
from nestor.handlers.notes import NotesHandler
from nestor.services.colorizer import Colorizer
from nestor.services.serializer import Serializer
from nestor.models.contacts_book import ContactsBook
from nestor.models.notes_book import NotesBook
from nestor.services.ui import CommandLineInterface

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = shlex.split(user_input)
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, *args

def help(command=None):
    commands = {
        "phone": "Show phone number by contact name. Example: phone <name>",
        "add-contact": "Add a contact. Example: add-contact <name> <phone>",
        "edit-contact": "Edit a contact. Example: edit-contact <name> <new phone>",
        "delete-contact": "Delete a contact. Example: delete-contact <name>",
        "show-birthday": "Show birthday by contact name. Example: show-birthday <name>",
        "add-birthday": "Add a birthday. Example: add-birthday <name> <date>",
        "birthdays": "Show upcoming birthdays. Example: birthdays <number of days>",
        "add-email": "Add an email. Example: add-email <name> <email>",
        "edit-email": "Edit an email. Example: edit-email <name> <new email>",
        "show-email": "Show email by contact name. Example: show-email <name>",
        "delete-email": "Delete an email. Example: delete-email <name>",
        "add-address": "Add an address. Example: add-address <name> <street> <city> <state> <zip_code> <country>",
        "edit-address": "Edit an address. Example: edit-address <name> <new street> <new city> <new state> <new zip_code> <new country>",
        "contacts": "Show all contacts. Example: contacts",
        "search-contacts": "Search contacts. Example: search-contacts <search string>"
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

    return Colorizer.info(help_message)


def main():
    # load ContactsBook and initialize contacts handler
    serializer = Serializer('data')
    ui = CommandLineInterface()
    storage = serializer.load_data()
    contacts_handler = ContactsHandler(storage.contacts_book)
    notes_handler = NotesHandler(storage.notes_book)

    ui.output(Colorizer.highlight("Welcome to the assistant bot!"))

    while True:
        user_input = ""
        try:
            user_input = input(Colorizer.info("Enter a command: "))
        # handle Exit on Ctrl+C
        except KeyboardInterrupt:
            ui.output(Colorizer.highlight("\nGood bye!"))
            serializer.save_data(storage)
            break

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            ui.output(Colorizer.highlight("Good bye!"))
            serializer.save_data(storage)
            break
        elif command == "hello":
            ui.output(Colorizer.highlight("How can I help you?"))
        elif command == "help":
            if args:
                ui.output(help(args[0]))
            else:
                ui.output(help())
        elif command in ContactsHandler.get_available_commands():
            ui.output(contacts_handler.handle(command, *args))
        elif command in NotesHandler.get_available_commands():
            ui.output(notes_handler.handle(command, *args))
        else:
            ui.output(Colorizer.error("Invalid command."))

if __name__ == "__main__":
    main()