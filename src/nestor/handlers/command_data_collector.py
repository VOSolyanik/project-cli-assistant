from typing import Callable, List, Optional

from nestor.models.exceptions import FieldRequiredError
from nestor.services.colorizer import Colorizer
from nestor.services.ui import UserInterface

class FieldInput:
    def __init__(self, prompt:str, default_value:str = "", validator:Callable = None, is_required:bool = False, children: Optional[List['FieldInput']] = None):
        self.prompt = prompt
        self.validator = validator
        self.is_required = is_required
        self.default_value = str(default_value) if default_value and str(default_value) else None
        self.children = children


def field_input(fields: list[FieldInput], cli: UserInterface, indent: int):
    """ Collects input from the user for a list of fields. """
    result = []
    for field in fields:
        while True:
            value = ""
            # If the field has children, recursively collect input for the children
            if field.children:
                cli.output(Colorizer.info(f"{' ' * indent}{field.prompt}: "))
                value = command_data_collector(field.children, cli, indent + 2)
            else:
                # Prompt the user for input, using the default value if provided
                value = yield (f"{' ' * indent}{field.prompt}: ", field.default_value if field.default_value else None)
                # Strip the value if it is not None
                value = value.strip() if value else None

            # If the value is empty and the field is required, raise an error
            if not value and field.is_required:
                yield FieldRequiredError(f"{field.prompt} is required")
                continue
            # If the value is not empty and a validator is provided, validate the value
            if value and field.validator:
                try:
                    field.validator(value)
                # If the validation fails, yield the exception and continue the loop for the same field
                except Exception as e:
                    yield e
                    continue
            # If the value is not empty, add it to the result list and break the loop
            result.append(value)
            break
    yield result

def command_data_collector(fields: list[FieldInput], cli: UserInterface, indent = 2) -> list[str | None]:
    """ Collects user input for the given fields. """
    generator = field_input(fields, cli, indent)
    prompt = next(generator)  # Initialize the generator
    default_value = None

    # Handle the case where the first prompt is a tuple, is for case when we have prompt and default value
    if isinstance(prompt, tuple):
        default_value = prompt[1]
        prompt = prompt[0]
    
    while True:
        user_input = ""
        try:
            # Prompt the user for input, using the default value if provided, and skip adding the input to the history
            user_input = cli.prompt(prompt, default_value, skip_history=True)

        # handle Exit on Ctrl+C
        except KeyboardInterrupt as e:
            cli.output("\n")
            raise e
            
        try:
            # Send the user input to the generator and get the next prompt
            prompt = generator.send(user_input)
            # If the prompt is a list, it means that the generator has finished collecting input
            if isinstance(prompt, list):
                e = StopIteration(prompt)
                raise e
            # If the prompt is an exception (validation failed), display the error message and get the next prompt
            if isinstance(prompt, Exception):
                cli.output(' ' * indent + Colorizer.error(prompt))
                prompt = next(generator)
            # If the prompt is a tuple, it means that we have a prompt and a default value
            if isinstance(prompt, tuple):
                default_value = prompt[1]
                prompt = prompt[0]
        except StopIteration as e:
            return list(e.value)
            