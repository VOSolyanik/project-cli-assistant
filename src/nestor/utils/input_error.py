from functools import wraps

from nestor.services.colorizer import Colorizer
from nestor.models.exceptions import ContactsBookException, NotesBookException

def input_error(errors_config: dict = {}):
    """
    Decorator that handles input errors and provides error messages.
    """
    errors = {
        ValueError: "Contact name and phone are required",
        IndexError: "Contact name is required"
    }

    errors.update(errors_config or {})

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError as e:
                return Colorizer.error(f"Contact {e} not found")
            except ContactsBookException as e:
                return Colorizer.error(e)            
            except NotesBookException as e:
                return Colorizer.error(e)
            except ValueError as e:
                return Colorizer.error(errors[ValueError])
            except IndexError as e:
                return Colorizer.error(errors[IndexError])
            except KeyboardInterrupt as e:
                return Colorizer.error(errors[KeyboardInterrupt])
        return inner
    return wrapper

