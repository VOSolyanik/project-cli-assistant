from typing import Callable
from enum import Enum
from colorama import Fore, Style

class ColorizeType(Enum):
	INFO = "info"
	WARNING = "warning"
	ERROR = "error"
	SUCCESS = "success"
	HIGHLIGHT = "highlight"

def colorize(type: ColorizeType) -> Callable:
	colors = {
		f"{ColorizeType.INFO.value}": Fore.BLUE,
		f"{ColorizeType.WARNING.value}": Fore.YELLOW,
		f"{ColorizeType.ERROR.value}": Fore.RED,
		f"{ColorizeType.SUCCESS.value}": Fore.GREEN,
		f"{ColorizeType.HIGHLIGHT.value}": Fore.MAGENTA,
	}
	def colorized(text: str):
		return f"{colors[type.value]}{text}{Style.RESET_ALL}"

	return colorized

class Colorizer:
	"""
	Colorize text output with colorama
	"""
	info = colorize(ColorizeType.INFO)
	warn = colorize(ColorizeType.WARNING)
	error = colorize(ColorizeType.ERROR)
	success = colorize(ColorizeType.SUCCESS)
	highlight = colorize(ColorizeType.HIGHLIGHT)
