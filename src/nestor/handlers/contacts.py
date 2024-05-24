import copy

from nestor.handlers.command_data_collector import FieldInput, command_data_collector
from nestor.models.constants import CONTACT_NOT_FOUND, PHONE_NOT_FOUND
from nestor.services.ui import UserInterface
from nestor.utils.csv_as_table import csv_as_table
from nestor.utils.get_days_range import get_days_range
from nestor.utils.input_error import input_error
from nestor.models.contacts_book import City, ContactsBook, Contact, Birthday, Country, Email, Name, Phone, State, ZipCode
from nestor.services.colorizer import Colorizer
from nestor.utils.similar_strings import similar_strings
from nestor.utils.to_csv import to_csv

class ContactsHandler():
    """
    Contacts handler class
    book: ContactsBook - contacts book instance
    """

    PHONE_COMMAND = "phone"
    ADD_PHONE_COMMAND = "add-phone"
    EDIT_PHONE_COMMAND = "edit-phone"
    DELETE_PHONE_COMMAND = "delete-phone"

    ADD_CONTACT_COMMAND = "add-contact"
    EDIT_CONTACT_COMMAND = "edit-contact"
    DELETE_CONTACT_COMMAND = "delete-contact"

    SHOW_BIRTHDAY_COMMAND = "show-birthday"
    ADD_BIRTHDAY_COMMAND = "add-birthday"

    ADD_EMAIL_COMMAND = "add-email"
    EDIT_EMAIL_COMMAND = "edit-email"
    SHOW_EMAIL_COMMAND = "show-email"
    DELETE_EMAIL_COMMAND = "delete-email"

    ADD_ADDRESS = "add-address"
    EDIT_ADDRESS = "edit-address"
    DELETE_ADDRESS = "delete-address"

    CONTACTS_COMMAND = "contacts"
    BIRTHDAYS_COMMAND = "birthdays"
    SEARCH_CONTACTS_COMMAND = "search-contacts"

    def __init__(self, book: ContactsBook, cli: UserInterface):
        self.book = book
        self.cli = cli

    @staticmethod
    def get_available_commands() -> list[str]:
        """
        Returns list of available commands
        """
        return [
            ContactsHandler.PHONE_COMMAND,
            ContactsHandler.ADD_PHONE_COMMAND,
            ContactsHandler.EDIT_PHONE_COMMAND,
            ContactsHandler.DELETE_PHONE_COMMAND,

            ContactsHandler.ADD_CONTACT_COMMAND,
            ContactsHandler.EDIT_CONTACT_COMMAND,
            ContactsHandler.DELETE_CONTACT_COMMAND,

            ContactsHandler.ADD_BIRTHDAY_COMMAND,
            ContactsHandler.SHOW_BIRTHDAY_COMMAND,
            ContactsHandler.BIRTHDAYS_COMMAND,

            ContactsHandler.ADD_EMAIL_COMMAND,
            ContactsHandler.EDIT_EMAIL_COMMAND,
            ContactsHandler.SHOW_EMAIL_COMMAND,

            ContactsHandler.DELETE_EMAIL_COMMAND,
            ContactsHandler.ADD_ADDRESS,
            ContactsHandler.EDIT_ADDRESS,
            ContactsHandler.DELETE_ADDRESS,

            ContactsHandler.CONTACTS_COMMAND,
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
            case ContactsHandler.ADD_PHONE_COMMAND:
                return self.__add_phone(*args)
            case ContactsHandler.EDIT_PHONE_COMMAND:
                return self.__edit_phone(*args)
            case ContactsHandler.DELETE_PHONE_COMMAND:
                return self.__delete_phone(*args)
            case ContactsHandler.DELETE_CONTACT_COMMAND:
                return self.__delete_contact(*args) 
            case ContactsHandler.ADD_CONTACT_COMMAND:
                return self.__add_contact()
            case ContactsHandler.EDIT_CONTACT_COMMAND:
                return self.__edit_contact(*args)
            case ContactsHandler.ADD_BIRTHDAY_COMMAND:
                return self.__add_contact_birthday(*args)
            case ContactsHandler.SHOW_BIRTHDAY_COMMAND:
                return self.__get_contact_birthday(*args)
            case ContactsHandler.BIRTHDAYS_COMMAND:
                return self.__get_upcoming_birthdays(*args)
            case ContactsHandler.CONTACTS_COMMAND:
                return self.__get_all_contacts()
            case ContactsHandler.ADD_EMAIL_COMMAND | ContactsHandler.EDIT_EMAIL_COMMAND:
                return self.__set_contact_email(*args)
            case ContactsHandler.SHOW_EMAIL_COMMAND:
                return self.__get_contact_email(*args)
            case ContactsHandler.DELETE_EMAIL_COMMAND:
                return self.__delete_contact_email(*args)
            case ContactsHandler.ADD_ADDRESS:
                return self.__add_address(*args)
            case ContactsHandler.EDIT_ADDRESS:
                return self.__edit_address(*args)
            case ContactsHandler.DELETE_ADDRESS:
                return self.__delete_address(*args)
            case ContactsHandler.SEARCH_CONTACTS_COMMAND:
                return self.__search_contacts(*args)
            case _:
                return Colorizer.error("Invalid command.")
            
    @input_error({KeyboardInterrupt: "Contact adding interrupted. Contact not added."})
    def __add_contact(self) -> str:
        """
        Adds contact to contacts dictionary
        """
        fields = [
            FieldInput(prompt="Name", validator=Name.validate, is_required=True),
            FieldInput(prompt="Phone number", validator=Phone.validate),
            FieldInput(prompt="Date of Birth", validator=Birthday.validate),
            FieldInput(prompt="Email", validator=Email.validate),
            FieldInput(prompt="Address", children=[
                FieldInput(prompt="Street"),
                FieldInput(prompt="City", validator=City.validate),
                FieldInput(prompt="State", validator=State.validate),
                FieldInput(prompt="Zip code", validator=ZipCode.validate),
                FieldInput(prompt="Country", validator=Country.validate),
            ]),
        ]

        name, phone, date, email, address = command_data_collector(fields, self.cli)

        phones = [phone] if phone else []

        existing_contact = self.book.find(name)

        if existing_contact is None:
            new_contact = Contact(name, phones, email=email, birthday=date)
            new_contact.add_address(*address)
            self.book.add(new_contact)
            return Colorizer.success(f"Contact {name} added.")
        else:
            if phone:
                existing_contact.add_phone(phone)
            if email:
                existing_contact.set_email(email)
            if date:
                existing_contact.set_birthday(date)
            if address:
                existing_contact.edit_address(*address)
                
            return Colorizer.success(f"Contact {name} updated.")
    
    @input_error({KeyboardInterrupt: "Contact editing interrupted. Contact not updated."})
    def __edit_contact(self, *args) -> str:
        """
        Edits contact in contacts dictionary
        """
        name = args[0]

        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)

        fields = [
            FieldInput(prompt="Name", default_value=contact.name, validator=Name.validate),
            FieldInput(prompt="Phone number", default_value=contact.phones[0] if contact.phones else "", validator=Phone.validate),
            FieldInput(prompt="Date of Birth", default_value=str(contact.birthday) if contact.birthday else None, validator=Birthday.validate),
            FieldInput(prompt="Email", default_value=contact.email, validator=Email.validate),
            FieldInput(prompt="Address", children=[
                FieldInput(prompt="Street", default_value=contact.address.street),
                FieldInput(prompt="City", default_value=contact.address.city, validator=City.validate),
                FieldInput(prompt="State", default_value=contact.address.state, validator=State.validate),
                FieldInput(prompt="Zip code", default_value=contact.address.zip_code, validator=ZipCode.validate),
                FieldInput(prompt="Country", default_value=contact.address.country, validator=Country.validate),
            ]),
        ]

        new_name, phone, date, email, address = command_data_collector(fields, self.cli)

        if new_name and new_name != str(contact.name) and self.book.find(new_name):
            return Colorizer.warn(f"Contact with name '{new_name}' already exist.")
        elif new_name and new_name != contact.name:
            contact = copy.deepcopy(contact)
            contact.rename(new_name)
            self.book.delete(name)
            self.book.add(contact)

        if phone:
            contact.add_phone(phone)
        if email:
            contact.set_email(email)
        if date:
            contact.set_birthday(date)
        if address:
            contact.edit_address(*address)

        return Colorizer.success(f"Contact {name} updated.")

    @input_error()
    def __delete_contact(self, *args) -> str:
        """
        Deletes a contact by name.
        args: list[str] - command arguments
        """
        
        name = args[0]
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        self.book.delete(name)
        return Colorizer.success(f"Contact {name} deleted.")
    
    @input_error()
    def __get_phones(self, *args) -> str:
        """
        Returns phone numbers for contact
        args: list[str] - command arguments
        """
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        return Colorizer.highlight("; ".join([str(item) for item in contact.phones]))
    
    @input_error({IndexError: "New phone is required"})
    def __add_phone(self, *args) -> str:
        """
        Add contact phone
        args: list[str] - command arguments
        """
        name, phone = args
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        existing_phone = contact.find_phone(phone)

        if existing_phone:
            return Colorizer.warn(f"Phone {phone} already exist for contact {name}")
        
        contact.add_phone(phone)
        return Colorizer.success(f"Contact {name} phone added.")
    
    @input_error({IndexError: "New phone is required"})
    def __edit_phone(self, *args) -> str:
        """
        Changes contact phone
        args: list[str] - command arguments
        """
        name, old_phone, *_ = args
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        phone = contact.find_phone(old_phone)
        
        if not phone:
            return Colorizer.warn(PHONE_NOT_FOUND)

        new_phone = args[2]
        phone.value = new_phone

        return Colorizer.success(f"Contact {name} phone changed.")
    
    @input_error()
    def __delete_phone(self, *args) -> str:
        """
        Changes contact phone
        args: list[str] - command arguments
        """
        name, phone = args
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        if not contact.find_phone(phone):
            return Colorizer.warn(PHONE_NOT_FOUND)

        contact.remove_phone(phone)

        return Colorizer.success(f"Contact {name} phone removed.")
    
    @input_error({ValueError: "Contact name and email are required"})
    def __set_contact_email(self, *args) -> str:
        """
        Edits or adds contact email
        args: list[str] - command arguments
        """
        name, email = args
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        contact.set_email(email)
        return Colorizer.success(f"Contact {name} email updated.")
    
    @input_error()
    def __get_contact_email(self, *args) -> str:
        """
        Returns email for contact
        args: list[str] - command arguments
        """
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        return Colorizer.success(str(contact.email))
    
    @input_error()
    def __delete_contact_email(self, *args) -> str:
        """
        Deletes email for contact
        args: list[str] - command arguments
        """
        name = args[0]
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        contact.remove_email()
        return Colorizer.success(f"Contact {name} email removed.")

    @input_error({ValueError: "Contact name and birthday are required"})
    def __add_contact_birthday(self, *args) -> str:
        """
        Adds birthday to contact
        args: list[str] - command arguments
        """
        name, birthday = args
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        contact.set_birthday(birthday)
        return Colorizer.success(f"Contact {name} birthday added.")
    
    @input_error()
    def __get_contact_birthday(self, *args) -> str:
        """
        Returns birthday for contact
        args: list[str] - command arguments
        """
        name = args[0]
        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        return Colorizer.success(str(contact.birthday))
    
    @input_error({ValueError: "Invalid period specified. Use 'tomorrow', 'this week', 'this month', 'next week', 'next month', or a non-negative number of days.", IndexError: "Number of days or period is required"})
    def __get_upcoming_birthdays(self, *args) -> str:
        """
        Returns all upcoming birthdays within the given period ('tomorrow', 'this week', 'this month', 'next week', 'next month') or number of days
        """
        
        period_mapping = {
            "tomorrow": (1, 1),
            "this week": get_days_range("this", "week"),
            "this month": get_days_range("this", "month"),
            "next week": get_days_range("next", "week"),
            "next month": get_days_range("next", "month")
        }
        
        period = " ".join(args).lower()
        if period in period_mapping:
            start_days, days = period_mapping[period]
        else:
            try:
                start_days = 0
                days = int(args[0])
                if days < 0:
                    raise ValueError("Days must be a non-negative integer.")
            except ValueError:
                raise ValueError("Invalid period specified. Use 'tomorrow', 'this week', 'this month', 'next week', 'next month', or a non-negative number of days.")
        
        birthdays = self.book.get_upcoming_birthdays(days, start_days)
        
        if not birthdays:
            return Colorizer.warn("No upcoming birthdays found.")
        
        return Colorizer.highlight("\n".join([f"Contact name: {name}, congratulate at: {date.strftime(Birthday.format)}" for name, date in birthdays.items()]))

    @input_error({ValueError: "Contact name is required to add address"})
    def __add_address(self, *args) -> str:
        """
        Adds address to contact
        args: list[str] - command arguments
        """

        name = args[0]

        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)

        fields = [
            FieldInput(prompt="Street", is_required=True),
            FieldInput(prompt="City", validator=City.validate, is_required=True),
            FieldInput(prompt="State", validator=State.validate),
            FieldInput(prompt="Zip code", validator=ZipCode.validate),
            FieldInput(prompt="Country", validator=Country.validate, is_required=True),
        ]

        street, city, state, zip_code, country = command_data_collector(fields, self.cli)

        contact.add_address(street, city, state, zip_code, country)

        return Colorizer.success(f"Contact {name} address added.")
    
    @input_error()
    def __edit_address(self, *args) -> str:
        """
        Edits address of contact
        args: list[str] - command arguments
        """
        name = args[0]

        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)

        fields = [
            FieldInput(prompt="Street", default_value=contact.address.street),
            FieldInput(prompt="City", default_value=contact.address.city, validator=City.validate),
            FieldInput(prompt="State", default_value=contact.address.state, validator=State.validate),
            FieldInput(prompt="Zip code", default_value=contact.address.zip_code, validator=ZipCode.validate),
            FieldInput(prompt="Country", default_value=contact.address.country, validator=Country.validate),
        ]

        address = command_data_collector(fields, self.cli)

        contact.edit_address(*address)

        return Colorizer.success(f"Contact {name} address updated.")
    
    @input_error()
    def __delete_address(self, *args) -> str:
        """
        Edits address of contact
        args: list[str] - command arguments
        """
        name = args[0]

        contact = self.book.find(name)

        if contact is None:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        contact.remove_address()

        return Colorizer.success(f"Contact {name} address removed.")
    
    
    @input_error({IndexError: "Search string is required"})
    def __search_contacts(self, *args) -> str:
        """
        Searches contacts by name, email and address. Performs fuzzy search if no results fount, to have suggestions.
        args: list[str] - command arguments
        """
        search_str = args[0]
        contacts = self.book.search(search_str)
        
        if not contacts:
            similar_names = similar_strings(search_str, self.book.data.keys(), 0.5)
            if not similar_names:
                return Colorizer.warn(CONTACT_NOT_FOUND)
            return Colorizer.warn(f"{CONTACT_NOT_FOUND} Did you mean: {similar_names[0]}?")
        
        return csv_as_table(to_csv(contacts))
        
    def __get_all_contacts(self) -> str:
        """
        Returns all contacts
        """
        if not self.book.data:
            return Colorizer.warn(CONTACT_NOT_FOUND)
        
        return csv_as_table(to_csv(list(self.book.data.values())))
    
