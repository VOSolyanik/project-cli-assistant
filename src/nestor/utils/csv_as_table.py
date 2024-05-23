import csv
from tabulate import tabulate

def csv_as_table(csv_string: str) -> str:
	"""
	Convert a CSV string into a formatted table.

	Args:
		csv_string (str): The CSV string to convert.

	Returns:
		str: The formatted table as a string.
	"""
	# Parse the CSV string
	reader = csv.reader(csv_string.strip().split('\n'), delimiter=';')
	headers = next(reader)  # Extract the first row as headers
	headers = list(map(lambda x: x.capitalize(), headers))
	rows = list(reader)     # Extract the remaining rows

	# Use tabulate to format the table
	table = tabulate(rows, headers, tablefmt='grid')
	
	# Return the formatted table
	return table
