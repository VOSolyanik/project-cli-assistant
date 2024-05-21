from functools import wraps
from services.colorizer import Colorizer
from models.exceptions import ContactsBookException

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
            except ValueError as e:
                return Colorizer.error(errors[ValueError])
            except IndexError as e:
                return Colorizer.error(errors[IndexError])
        return inner
    return wrapper

