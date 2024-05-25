class FieldRequiredError(Exception):
    pass

class ContactsBookException(Exception):
    pass

class NameValueError(ContactsBookException):
    pass

class PhoneValueError(ContactsBookException):
    pass

class BirthdayValueError(ContactsBookException):
    pass

class EmailValueError(ContactsBookException):
    pass

class AddressValueError(ContactsBookException):
    pass

class NotesBookException(Exception):
    pass

class TitleValueError(NotesBookException):
    pass

class ContentValueError(NotesBookException):
    pass