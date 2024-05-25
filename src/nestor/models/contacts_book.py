import re
from collections import UserDict
from datetime import datetime, timedelta, date

from nestor.models.constants import EMPTY_FIELD_VALUE
from nestor.models.exceptions import AddressValueError, NameValueError, PhoneValueError, BirthdayValueError, EmailValueError

class Field:
    """Base class for fields."""
    def __init__(self, value: str):
        self._value = None
        self.value = value
    
    def __str__(self):
        return str(self._value) if self._value else ""
    
    def __repr__(self):
        return str(self)
    
class Name(Field):
    """Class representing a name field."""

    @staticmethod
    def validate(value: str) -> None:
        if value is None or len(value) == 0:
            raise NameValueError("Name is required")
                                 
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        Name.validate(value)
        
        self._value = value

class Phone(Field):
    """Class representing a phone field."""

    @staticmethod
    def validate(value: str) -> None:
        if not value.isdigit():
            raise PhoneValueError("Phone number must contain only digits")
        
        if len(value) != 10:
            raise PhoneValueError("Phone number must contain 10 digits")
        
    @property
    def value(self):
        return self._value 
    
    @value.setter
    def value(self, value: str):
        Phone.validate(value)
        
        self._value = value

class Email(Field):
    """Class representing a email field."""
    format_regexp = r'^\S+@\S+\.\S+$'

    @staticmethod
    def validate(value: str) -> None:
        if re.match(Email.format_regexp, value) is None:
            raise EmailValueError("Wrong email format")
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        Email.validate(value)
        
        self._value = value

class Birthday(Field):
    """Class representing a birthday field."""
    format = '%d.%m.%Y'

    def __str__(self):
        return self.value.strftime(Birthday.format)
    
    @staticmethod
    def parse(value: str) -> date:
        return datetime.strptime(value, Birthday.format).date()

    @staticmethod
    def validate(value: str) -> datetime:
        try:
            Birthday.parse(value)
        except ValueError as exc:
            raise BirthdayValueError("Invalid date format. Use DD.MM.YYYY") from exc

    @property
    def value(self):
        return self._value 
    
    @value.setter
    def value(self, value: str):
        Birthday.validate(value)

        self._value = Birthday.parse(value)

class Street(Field):
    """Class representing street name from address."""

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        self._value = value

class City(Field):
    """Class representing city from address."""

    @staticmethod
    def validate(value: str) -> None:
        if not value[0].isupper():
            raise AddressValueError("City name should start with capital letter")
                                 
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        City.validate(value)
        
        self._value = value

class State(Field):
    """Class representing state from address."""

    @staticmethod
    def validate(value: str) -> None:
        if not value[0].isupper():
            raise AddressValueError("State name should start with capital letter")
                 
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        self._value = value

class ZipCode(Field):
    """Class representing zip code from address."""

    @staticmethod
    def validate(value: str) -> None:
        if not value.isdigit():
            raise AddressValueError("Zip code must contain only digits")
                                 
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        ZipCode.validate(value)
        
        self._value = value

class Country(Field):
    """Class representing country from address."""

    @staticmethod
    def validate(value: str) -> None:
        if not value[0].isupper():
            raise AddressValueError("Country name should start with capital letter")
                                 
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        Country.validate(value)
        
        self._value = value
        
class Address:
    def __init__(self, street: str = None, city: str = None, state: str = None, zip_code: str = None, country: str = None):
        self.street = Street(street) if street else None
        self.city = City(city) if city else None
        self.state = State(state) if state else None
        self.zip_code = ZipCode(zip_code) if zip_code else None
        self.country = Country(country) if country else None

    def edit(self, street: str = None, city: str = None, state: str = None, zip_code: str = None, country: str = None):
        self.street = Street(street) if street else self.street
        self.city = City(city) if city else self.city
        self.state = State(state) if state else self.state
        self.zip_code = ZipCode(zip_code) if zip_code else self.zip_code
        self.country = Country(country) if country else self.country

    def __str__(self):
        fields: list[Field] = [self.street, self.city, self.state, self.zip_code, self.country]
        return ', '.join([str(f) for f in fields if f is not None])
    
class Contact:
    """Contact class for storing contact information."""
    def __init__(self, name, phones=None, email=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(p) for p in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None
        self.email = Email(email) if email else None
        self.address = None

    def __str__(self):
        return f"Name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday or EMPTY_FIELD_VALUE}, email: {self.email or EMPTY_FIELD_VALUE}, address: {self.address or EMPTY_FIELD_VALUE}"
    
    def rename(self, new_name: str) -> None:
        """Rename contact."""
        self.name = Name(new_name)

    def add_phone(self, phone: str) -> None:
        """Add phone to record if it's valid, otherwise handle ValueError."""
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit phone in record if it exists."""
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def remove_phone(self, phone: str) -> None:
        """Remove phone from record if it exists."""
        self.phones = [p for p in self.phones if p.value != phone]

    def find_phone(self, phone: str) -> Phone | None:
        """Find phone in record by value, return None if not found."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def set_email(self, email: str) -> None:
        """Edit email in record."""
        self.email = Email(email)

    def remove_email(self) -> None:
        """Remove email from record."""
        self.email = None
    
    def set_birthday(self, birthday: str) -> None:
        """Add birthday to record if it's valid, otherwise handle ValueError."""
        self.birthday = Birthday(birthday)

    def add_address(self, street: str, city: str, state: str, zip_code: str, country: str):
        """Add address"""
        self.address = Address(street, city, state, zip_code, country)

    def edit_address(self, street: str = None, city: str = None, state: str = None, zip_code: str = None, country: str = None):
        """Edit address"""
        if not self.address:
            self.address = Address(street, city, state, zip_code, country)
        else:
            self.address.edit(street, city, state, zip_code, country)

    def remove_address(self):
        """Remove address from record."""
        self.address = None
    

class ContactsBook(UserDict):
    """Class representing a contacts book."""
    def add(self, record: Contact) -> None:
        """Add record to address book."""
        self.data[record.name.value] = record
    
    def delete(self, name: str) -> None:
        """Delete record from address book by name."""
        del self.data[name]
        
    def find(self, name: str) -> Contact | None:
        """Find record in address book by name, return None if not found."""
        if name in self.data:
            return self.data[name]
        return None
    
    def search(self, search_str: str) -> list[Contact]:
        """Search records in address book by name, email and address."""

        result = []
        for record in self.data.values():
            if search_str.lower() in str(record.name).lower() or \
                (record.email and search_str.lower() in record.email.value.lower()) or \
                    (record.address and search_str.lower() in str(record.address).lower()):
                result.append(record)
        return result
    
    def get_upcoming_birthdays(self, days: int, start_days: int = 0) -> dict:
        """Return dict of contacts with upcoming birthdays within the given number of days starting from start_days."""
        today = datetime.today().date()
        start_date = today + timedelta(days=start_days)
        upcoming_birthdays = {}
        
        # Iterate through all users
        for record in self.data.values():
            if record.birthday is None:
                continue

            birthdate: datetime = record.birthday.value
            name: str = record.name.value
            # Calculate this year's birthday
            birthdate_this_year = birthdate.replace(year=today.year)
            # If this year's birthday in past, calculate next year's birthday
            if birthdate_this_year < today:
                birthdate_this_year = birthdate.replace(year=today.year + 1)

            # Calculate days to birthday
            days_to_birthday = (birthdate_this_year - today).days

            if start_days <= days_to_birthday <= start_days + days:
                congratulation_date = birthdate_this_year
                # If congratulation date is weekend, calculate next week's date
                if birthdate_this_year.weekday() >= 5:
                    congratulation_date += timedelta(days=(7 - congratulation_date.weekday()))
                # Add user to upcoming birthdays dict
                upcoming_birthdays[name] = congratulation_date

        return upcoming_birthdays
