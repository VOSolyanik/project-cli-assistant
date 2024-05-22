class ContactsBookException(Exception):
    pass

class PhoneValueError(ContactsBookException):
    pass

class BirthdayValueError(ContactsBookException):
    pass

class EmailValueError(ContactsBookException):
    pass

class AddressValueError(ContactsBookException):
    pass
