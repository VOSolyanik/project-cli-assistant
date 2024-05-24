
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, WordCompleter, PathCompleter

class ContextualCompleter(Completer):
    def __init__(self, commands: list[str]):
        # Define command completers
        self.command_completer = WordCompleter(commands, ignore_case=True)
        # Define path completer for file system paths
        self.path_completer = PathCompleter()

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        words = text_before_cursor.split()

        if len(words) == 1 and text_before_cursor.strip() == text_before_cursor:
            # Provide command completions for the first word
            return self.command_completer.get_completions(document, complete_event)
        else:

            # Provide path completions for subsequent words
            return self.path_completer.get_completions(document, complete_event)
        

class UserInterface:
    def output(self, text: str) -> None:
        pass

    def prompt(self, text: str, default_value: str = None, completion: list[str] = None) -> str:
        pass

class CommandLineInterface(UserInterface):
    """
    A class representing a command-line interface for user interaction.

    This class inherits from the UserInterface class and provides methods for outputting text and prompting the user for input.

    Attributes:
        None

    Methods:
        output(text: str) -> None: Outputs the given text to the command line.
        prompt(text: str, completion: list[str]) -> str: Prompts the user with the given text and a list of possible completions, and returns the user's input as a string.
    """
    style = Style.from_dict({
        'prompt': '#0000ab',
        'input': '#000000'
    })

    def output(self, text: str) -> None:
        """ Prints the given text."""
        print(text)

    def prompt(self, text: str, default_value: str = None, completion: list[str] = None) -> str:
        return prompt(
                message=text,
                default=default_value if default_value else "",
                completer=ContextualCompleter(completion if completion else []),
                style=CommandLineInterface.style
            )
