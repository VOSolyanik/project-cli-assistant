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
            if field.children:
                cli.output(Colorizer.info(f"{' ' * indent}{field.prompt}: "))
                value = command_data_collector(field.children, cli, indent + 2)
            else:
                value = yield (f"{' ' * indent}{field.prompt}: ", field.default_value if field.default_value else None)
                value = value.strip() if value else None

            if not value and field.is_required:
                yield FieldRequiredError(f"{field.prompt} is required")
                continue
            if value and field.validator:
                try:
                    field.validator(value)
                except Exception as e:
                    yield e
                    continue
            result.append(value)
            break
    yield result

def command_data_collector(fields: list[FieldInput], cli: UserInterface, indent = 2) -> list[str | None]:
    """ Collects user input for the given fields. """
    generator = field_input(fields, cli, indent)
    prompt = next(generator)  # Initialize the generator
    default_value = None

    if isinstance(prompt, tuple):
        default_value = prompt[1]
        prompt = prompt[0]
    
    while True:
        user_input = ""
        try:
            user_input = cli.prompt(prompt, default_value, skip_history=True)

        # handle Exit on Ctrl+C
        except KeyboardInterrupt as e:
            cli.output("\n")
            raise e
            
        try:
            prompt = generator.send(user_input)
            if isinstance(prompt, list):
                e = StopIteration(prompt)
                raise e
            if isinstance(prompt, Exception):
                cli.output(' ' * indent + Colorizer.error(prompt))
                prompt = next(generator)
            if isinstance(prompt, tuple):
                default_value = prompt[1]
                prompt = prompt[0]
        except StopIteration as e:
            return e.value
    return []
            