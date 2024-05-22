from typing import Dict
from datetime import datetime

from nestor.utils.input_error import input_error
from nestor.models.contacts_book import ContactsBook, Contact, Birthday
from nestor.services.colorizer import Colorizer
from nestor.models.exceptions import AddressValueError

class ContactsHandler():
    PHONE_COMMAND = "phone"
    ADD_COMMAND = "add"
    CHANGE_COMMAND = "change"
    ADD_BIRTHDAY_COMMAND = "add-birthday"
    ADD_EMAIL_COMMAND = "add-email"
    EDIT_EMAIL_COMMAND = "edit-email"
    SHOW_EMAIL_COMMAND = "show-email"
    DELETE_EMAIL_COMMAND = "delete-email"
    SHOW_BIRTHDAY_COMMAND = "show-birthday"
    BIRTHDAYS_COMMAND = "birthdays"
    ALL_COMMAND = "all"
    ADD_ADDRESS = "add-address"
    EDIT_ADDRESS = "edit-address"

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
            ContactsHandler.PHONE_COMMAND,
            ContactsHandler.ADD_COMMAND,
            ContactsHandler.CHANGE_COMMAND,
            ContactsHandler.ADD_BIRTHDAY_COMMAND,
            ContactsHandler.ADD_EMAIL_COMMAND,
            ContactsHandler.EDIT_EMAIL_COMMAND,
            ContactsHandler.SHOW_EMAIL_COMMAND,
            ContactsHandler.DELETE_EMAIL_COMMAND,
            ContactsHandler.SHOW_BIRTHDAY_COMMAND,
            ContactsHandler.BIRTHDAYS_COMMAND,
            ContactsHandler.ALL_COMMAND,
            ContactsHandler.ADD_ADDRESS,
            ContactsHandler.EDIT_ADDRESS
        ]

    def handle(self, command: str, *args: list[str]) -> str:
        """
        Handles user commands
        command: str - user command
        args: list[str] - command arguments
        """
        match command:
            case ContactsHandler.PHONE_COMMAND:
                return self.__get_phones(*args)
            case ContactsHandler.ADD_COMMAND:
                return self.__add_contact(*args)
            case ContactsHandler.CHANGE_COMMAND:
                return self.__change_contact(*args)
            case ContactsHandler.ADD_BIRTHDAY_COMMAND:
                return self.__add_birthday(*args)
            case ContactsHandler.SHOW_BIRTHDAY_COMMAND:
                return self.__show_birthday(*args)
            case ContactsHandler.BIRTHDAYS_COMMAND:
                return self.__get_upcoming_birthdays(*args)
            case ContactsHandler.ALL_COMMAND:
                return self.__get_all_contacts()
            case ContactsHandler.EDIT_EMAIL_COMMAND | ContactsHandler.ADD_EMAIL_COMMAND:
                return self.__edit_email(*args)
            case ContactsHandler.SHOW_EMAIL_COMMAND:
                return self.__show_email(*args)
            case ContactsHandler.DELETE_EMAIL_COMMAND:
                return self.__delete_email(*args)
            case ContactsHandler.ADD_ADDRESS:
                return self.__add_address(*args)
            case ContactsHandler.EDIT_ADDRESS:
                return self.__edit_address(*args)
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
    
    @input_error({ValueError: "Contact name and email are required"})
    def __edit_email(self, *args) -> str:
        """
        Edits or adds contact email
        args: list[str] - command arguments
        """
        name, email = args
        record = self.book.find(name)
        message = Colorizer.success(f"Contact {name} email updated.")

        if record is None:
            return Colorizer.warn("Contact not found")
        
        record.edit_email(email)
        return message
    
    @input_error()
    def __show_email(self, *args) -> str:
        """
        Returns email for contact
        args: list[str] - command arguments
        """
        name = args[0]
        record = self.book.find(name)
        if record is None:
            return Colorizer.warn("Contact not found")
        
        return Colorizer.success(str(record.email))
    
    @input_error()
    def __delete_email(self, *args) -> str:
        """
        Deletes email for contact
        args: list[str] - command arguments
        """
        name = args[0]
        record = self.book.find(name)
        message = Colorizer.success(f"Contact {name} email removed.")

        if record is None:
            return Colorizer.warn("Contact not found")
        
        record.remove_email()
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
    
    @input_error({ValueError: "Days must be a non-negative integer.", IndexError: "Number of days is required"})
    def __get_upcoming_birthdays(self, *args) -> str:
        """
        Returns all upcoming birthdays within the given number of days
        """
        
        days = int(args[0])
        birthdays = self.book.get_upcoming_birthdays(days)
        
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
    
    @input_error()
    def __add_address(self, *args) -> str:
        """
        Adds address to contact
        args: list[str] - command arguments
        """
        if len(args) != 6:
            raise AddressValueError("All address fields must be provided.")
        name, street, city, state, zip_code, country = args
        contact = self.book.find(name)
        if contact is None:
            return Colorizer.error(f"Contact not found")
        contact.add_address(street, city, state, zip_code, country)
        return Colorizer.success(f"Contact {name} address added.")

    @input_error()
    def __edit_address(self, *args) -> str:
        """
        Edits address of contact
        args: list[str] - command arguments
        """
        if len(args) != 6:
            raise AddressValueError("All address fields must be provided.")
        name, street, city, state, zip_code, country = args
        contact = self.book.find(name)
        if contact is None:
            return Colorizer.error(f"Contact not found")
        contact.edit_address(street, city, state, zip_code, country)
        return Colorizer.success(f"Contact {name} address updated successfully.")
