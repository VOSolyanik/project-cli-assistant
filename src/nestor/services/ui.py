class UserInterface:
    def output(self, text: str) -> None:
        pass

    def input(self, text: str) -> str:
        pass

class CommandLineInterface(UserInterface):
    def output(self, text: str) -> None:
        print(text)

    def input(self, text: str) -> str:
        return input(text)