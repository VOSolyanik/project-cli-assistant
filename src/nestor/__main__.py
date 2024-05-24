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

def help_handler(contacts_handler, notes_handler, command=None):
    if command:
        if command in ContactsHandler.get_available_commands():
            return contacts_handler.help(command)
        elif command in NotesHandler.get_available_commands():
            return notes_handler.help(command)
        else:
            return "No help available for that command."
    else:
        return ("Available sections:\n"
                "1. Contacts\n"
                "2. Notes\n"
                "Please specify the section you need help with by typing 'help contacts' or 'help notes'.\n"
                "You can also get information about a specific command by typing 'help <command>'. For example, 'help add-note'.")

def section_help_handler(contacts_handler, notes_handler, section):
    if section == "contacts":
        return contacts_handler.help()
    elif section == "notes":
        return notes_handler.help()
    else:
        return "Invalid section. Please choose 'contacts' or 'notes'."

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
                if args[0] in ["contacts", "notes"]:
                    ui.output(Colorizer.info(section_help_handler(contacts_handler, notes_handler, args[0])))
                else:
                    help_message = help_handler(contacts_handler, notes_handler, args[0])
                    ui.output(Colorizer.info(help_message))
            else:
                help_message = help_handler(contacts_handler, notes_handler)
                ui.output(Colorizer.info(help_message))
        elif command in ContactsHandler.get_available_commands():
            ui.output(contacts_handler.handle(command, *args))
        elif command in NotesHandler.get_available_commands():
            ui.output(notes_handler.handle(command, *args))
        else:
            ui.output(Colorizer.error("Invalid command."))

if __name__ == "__main__":
    main()