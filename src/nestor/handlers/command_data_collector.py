from collections import namedtuple

from nestor.models.exceptions import FieldRequiredError
from nestor.services.colorizer import Colorizer

FieldInput = namedtuple("FieldInput", ["prompt", "validator", "is_required"])

def contact_input(fields: list[FieldInput]):
    """
    Collects input from the user for a list of fields.

    Args:
        fields (list[FieldInput]): A list of FieldInput objects representing the fields to collect input for.

    Yields:
        Union[str, FieldRequiredError, Exception, list[str]]: Yields prompts for each field, and handles validation and error handling.

    Returns:
        list[str]: A list of collected input values for each field.
    """
    result = []
    for field in fields:
        while True:
            value = yield f"{field.prompt}: "
            if not value and field.is_required:
                yield FieldRequiredError(f"{field.prompt} is required")
                continue
            if value and field.validator:
                try:
                    field.validator(value)
                except Exception as e:
                    yield e
                    continue
            result.append(value.strip() if value else None)
            break
    yield result

def command_data_collector(fields: list[FieldInput]) -> list[str | None]:
    """
    Collects user input for the given fields.

    Args:
        fields (list[FieldInput]): A list of FieldInput objects representing the fields to collect data for.

    Returns:
        Any: The collected data.

    Raises:
        StopIteration: If the generator is exhausted and returns a value.
    """
    generator = contact_input(fields)
    prompt = next(generator)  # Initialize the generator
    
    while True:
        user_input = ""
        try:
            user_input = input(Colorizer.highlight(prompt))

        # handle Exit on Ctrl+C
        except KeyboardInterrupt:
            print("\n")
            break
            
        try:
            prompt = generator.send(user_input)
            if isinstance(prompt, list):
                e = StopIteration(prompt)
                raise e
            if isinstance(prompt, Exception):
                print(Colorizer.error(prompt))
                prompt = next(generator)
        except StopIteration as e:
            return e.value
    return []
            