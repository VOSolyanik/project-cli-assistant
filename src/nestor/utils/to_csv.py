def to_csv(data_list: list) -> str:
    """
    Converts list to CSV format
    contacts: list[Contact] - list of contacts
    """
    header = ";".join(data_list[0].__dict__.keys())
    rows = []
    for contact in data_list:
        row = []
        for value in contact.__dict__.values():
            if isinstance(value, list):
                row.append(",".join([str(item) for item in value]))
            else:
                row.append(str(value))
        rows.append(";".join(row))
    return header + "\n" + "\n".join(rows)
