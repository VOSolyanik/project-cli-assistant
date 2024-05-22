from nestor.handlers.command_data_collector import FieldInput, command_data_collector
from nestor.utils.csv_as_table import csv_as_table
from nestor.utils.input_error import input_error
from nestor.models.contacts_book import ContactsBook, Contact, Birthday, Email, Field, Name, Phone
from nestor.services.colorizer import Colorizer
from nestor.models.exceptions import AddressValueError
from nestor.utils.to_csv import to_csv

class ContactsHandler():
    """
    Contacts handler class
    book: ContactsBook - contacts book instance
    """

    PHONE_COMMAND = "phone"

    ADD_CONTACT_COMMAND = "add-contact"
    EDIT_CONTACT_COMMAND = "edit-contact"
    DELETE_CONTACT_COMMAND = "delete-contact"

    SHOW_BIRTHDAY_COMMAND = "show-birthday"
    ADD_BIRTHDAY_COMMAND = "add-birthday"
    BIRTHDAYS_COMMAND = "birthdays"

    ADD_EMAIL_COMMAND = "add-email"
    EDIT_EMAIL_COMMAND = "edit-email"
    SHOW_EMAIL_COMMAND = "show-email"
    DELETE_EMAIL_COMMAND = "delete-email"

    ADD_ADDRESS = "add-address"
    EDIT_ADDRESS = "edit-address"

    CONTACTS_COMMAND = "contacts"
    SEARCH_CONTACTS_COMMAND = "search-contacts"

    def __init__(self, book: ContactsBook):
        self.book = book

    @staticmethod
    def get_available_commands() -> list[str]:
        """
        Returns list of available commands
        """
        return [
            ContactsHandler.PHONE_COMMAND,
            ContactsHandler.DELETE_CONTACT_COMMAND,
            ContactsHandler.ADD_CONTACT_COMMAND,
            ContactsHandler.EDIT_CONTACT_COMMAND,
            ContactsHandler.ADD_BIRTHDAY_COMMAND,
            ContactsHandler.ADD_EMAIL_COMMAND,
            ContactsHandler.EDIT_EMAIL_COMMAND,
            ContactsHandler.SHOW_EMAIL_COMMAND,
            ContactsHandler.DELETE_EMAIL_COMMAND,
            ContactsHandler.SHOW_BIRTHDAY_COMMAND,
            ContactsHandler.BIRTHDAYS_COMMAND,
            ContactsHandler.CONTACTS_COMMAND,
            ContactsHandler.ADD_ADDRESS,
            ContactsHandler.EDIT_ADDRESS,
            ContactsHandler.SEARCH_CONTACTS_COMMAND
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
            case ContactsHandler.DELETE_CONTACT_COMMAND:
                return self.__delete_contact(*args) 
            case ContactsHandler.ADD_CONTACT_COMMAND:
                return self.__add_contact()
            case ContactsHandler.EDIT_CONTACT_COMMAND:
                return self.__edit_contact(*args)
            case ContactsHandler.ADD_BIRTHDAY_COMMAND:
                return self.__add_birthday(*args)
            case ContactsHandler.SHOW_BIRTHDAY_COMMAND:
                return self.__show_birthday(*args)
            case ContactsHandler.BIRTHDAYS_COMMAND:
                return self.__get_upcoming_birthdays(*args)
            case ContactsHandler.CONTACTS_COMMAND:
                return self.__get_all_contacts()
            case ContactsHandler.ADD_EMAIL_COMMAND | ContactsHandler.EDIT_EMAIL_COMMAND:
                return self.__set_email(*args)
            case ContactsHandler.SHOW_EMAIL_COMMAND:
                return self.__show_email(*args)
            case ContactsHandler.DELETE_EMAIL_COMMAND:
                return self.__delete_email(*args)
            case ContactsHandler.ADD_ADDRESS:
                return self.__add_address(*args)
            case ContactsHandler.EDIT_ADDRESS:
                return self.__edit_address(*args)
            case ContactsHandler.SEARCH_CONTACTS_COMMAND:
                return self.__search_contacts(*args)
            case _:
                return Colorizer.error("Invalid command.")
    
    @input_error()
    def __get_phones(self, *args) -> str:
        """
        Returns phone numbers for contact
        args: list[str] - command arguments
        """
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return Colorizer.warn("Contact not found")
        
        return Colorizer.highlight("; ".join([str(item) for item in contact.phones]))
    

    @input_error({ValueError: "Contact adding interrupted. Contact not added."})
    def __add_contact(self) -> str:
        """
        Adds contact to contacts dictionary
        """

        fields = [
            FieldInput(prompt="Name", validator=Name.validate, is_required=True),
            FieldInput(prompt="Phone number", validator=Phone.validate, is_required=False),
            FieldInput(prompt="Date of Birth", validator=Birthday.validate, is_required=False),
            FieldInput(prompt="Email", validator=Email.validate, is_required=False),
        ]

        name, phone, date, email = command_data_collector(fields)
        phones = [phone] if phone else []

        existing_contact = self.book.find(name)

        if existing_contact is None:
            new_contact = Contact(name, phones, email=email, birthday=date)
            self.book.add(new_contact)
            message = Colorizer.success(f"Contact {name} added.")
        else:
            if phone:
                existing_contact.add_phone(phone)
            if email:
                existing_contact.set_email(email)
            if date:
                existing_contact.set_birthday(date)
            message = Colorizer.success(f"Contact {name} updated.")

        return message

    @input_error({IndexError: "New phone is required"})
    def __edit_contact(self, *args) -> str:
        """
        Changes contact phone
        args: list[str] - command arguments
        """
        name, old_phone, *_ = args
        contact = self.book.find(name)
        phone = contact.find_phone(old_phone)
        message = Colorizer.success(f"Contact {name} phone changed.")

        if contact is None:
            message = Colorizer.warn("Contact not found.")
        if phone is None:
            message = Colorizer.warn("Phone not found.")
        if phone:
            new_phone = args[2]
            phone.value = new_phone

        return message
    
    @input_error({ValueError: "Contact name and email are required"})
    def __set_email(self, *args) -> str:
        """
        Edits or adds contact email
        args: list[str] - command arguments
        """
        name, email = args
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn("Contact not found")
        
        contact.set_email(email)
        return Colorizer.success(f"Contact {name} email updated.")
    
    @input_error()
    def __show_email(self, *args) -> str:
        """
        Returns email for contact
        args: list[str] - command arguments
        """
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return Colorizer.warn("Contact not found")
        
        return Colorizer.success(str(contact.email))
    
    @input_error()
    def __delete_email(self, *args) -> str:
        """
        Deletes email for contact
        args: list[str] - command arguments
        """
        name = args[0]
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn("Contact not found")
        
        contact.remove_email()
        return Colorizer.success(f"Contact {name} email removed.")

    @input_error({ValueError: "Contact name and birthday are required"})
    def __add_birthday(self, *args) -> str:
        """
        Adds birthday to contact
        args: list[str] - command arguments
        """
        name, birthday = args
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn("Contact not found")
        
        contact.set_birthday(birthday)
        return Colorizer.success(f"Contact {name} birthday added.")
    
    @input_error()
    def __show_birthday(self, *args) -> str:
        """
        Returns birthday for contact
        args: list[str] - command arguments
        """
        name = args[0]
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn("Contact not found")
        
        return Colorizer.success(str(contact.birthday))
    
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
        
        return csv_as_table(to_csv(list(self.book.data.values())))
    
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
            return Colorizer.error("Contact not found")
        
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
            return Colorizer.error("Contact not found")
        
        contact.edit_address(street, city, state, zip_code, country)
        return Colorizer.success(f"Contact {name} address updated successfully.")
    
    @input_error()
    def __delete_contact(self, *args) -> str:
        """
        Deletes a contact by name.
        args: list[str] - command arguments
        """
        
        name = args[0]
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn("Contact not found")
        
        self.book.delete(name)
        return Colorizer.success(f"Contact {name} deleted.")
    
    @input_error({IndexError: "Search string is required"})
    def __search_contacts(self, *args) -> str:
        """
        Searches contacts by name, email and address
        args: list[str] - command arguments
        """
        search_str = args[0]
        contacts = self.book.search(search_str)
        
        if not contacts:
            return Colorizer.warn("No contacts found")
        
        return csv_as_table(to_csv(contacts))

