from typing import Dict
from datetime import datetime
from utils.input_error import input_error
from models.contacts_book import ContactsBook, Contact, Birthday
from services.colorizer import Colorizer

class ContactsHandler():
    """
    Contacts handler class
    book: ContactsBook - contacts book instance
    """
    def __init__(self, book: ContactsBook):
        self.book = book

    @staticmethod
    def get_available_commands() -> list[str]:
        """
        Returns list of available commands
        """
        return [
            "phone",
            "add",
            "change",
            "add-birthday",
            "show-birthday",
            "birthdays",
            "all"
        ]

    def handle(self, command: str, *args: list[str]) -> str:
        """
        Handles user commands
        command: str - user command
        args: list[str] - command arguments
        """
        match command:
            case "phone":
                return self.__get_phones(*args)
            case "add":
                return self.__add_contact(*args)
            case "change":
                return self.__change_contact(*args)
            case "add-birthday":
                return self.__add_birthday(*args)
            case "show-birthday":
                return self.__show_birthday(*args)
            case "birthdays":
                return self._get_birthdays()
            case "all":
                return self.__get_all_contacts()
            case _:
                return Colorizer.error("Invalid command.")
    
    @input_error()
    def __get_phones(self, *args) -> str:
        """
        Returns phone numbers for contact
        args: list[str] - command arguments
        """
        name = args[0]
        record = self.book.find(name)
        if record is None:
            return Colorizer.warn("Contact not found")
        
        return Colorizer.highlight("; ".join([str(item) for item in record.phones]))
    
    @input_error()
    def __add_contact(self, *args) -> str:
        """
        Adds contact to contacts dictionary
        args: list[str] - command arguments
        """
        name, phone = args
        record = self.book.find(name)
        message = Colorizer.success(f"Contact {name} updated.")

        if record is None:
            record = Contact(name)
            record.add_phone(phone)
            self.book.add_record(record)
            message = Colorizer.success(f"Contact {name} added.")
        else:
            record.add_phone(phone)

        return message

    @input_error({IndexError: "New phone is required"})
    def __change_contact(self, *args) -> str:
        """
        Changes contact phone
        args: list[str] - command arguments
        """
        name, old_phone, *_ = args
        record = self.book.find(name)
        phone = record.find_phone(old_phone)
        message = Colorizer.success(f"Contact {name} phone changed.")

        if record is None:
            message = Colorizer.warn(f"Contact not found.")
        if phone is None:
            message = Colorizer.warn(f"Phone not found.")
        if phone:
            new_phone = args[2]
            phone.value = new_phone

        return message

    @input_error({ValueError: "Contact name and birthday are required"})
    def __add_birthday(self, *args) -> str:
        """
        Adds birthday to contact
        args: list[str] - command arguments
        """
        name, birthday = args
        record = self.book.find(name)
        message = Colorizer.success(f"Contact {name} birthday added.")

        if record is None:
            return Colorizer.warn("Contact not found")
        
        record.add_birthday(birthday)
        return message
    
    @input_error()
    def __show_birthday(self, *args) -> str:
        """
        Returns birthday for contact
        args: list[str] - command arguments
        """
        name = args[0]
        record = self.book.find(name)
        if record is None:
            return Colorizer.warn("Contact not found")
        
        return Colorizer.success(str(record.birthday))
    
    @input_error()
    def _get_birthdays(self) -> str:
        """
        Returns all upcoming birthdays
        """
        birthdays: Dict[str, datetime] = self.book.get_upcoming_birthdays()

        if not birthdays:
            return Colorizer.warn("No upcoming birthdays found.")
        
        return Colorizer.highlight("\n".join([f"Contact name: {name}, congratulate at: {date.strftime(Birthday.format)}" for name, date in birthdays.items()]))
    
    def __get_all_contacts(self) -> str:
        """
        Returns all contacts
        """
        if not self.book.data:
            return Colorizer.warn("No contacts found")
        
        return Colorizer.highlight("\n".join([str(record) for record in self.book.data.values()]))
    
