from datetime import datetime, timedelta

def get_days_range(this_or_next, week_or_month):
    """ Returns the start and end days of the week or month. """
    today = datetime.today()
    
    if week_or_month == "week":
        if this_or_next == "this":
            start_days = 0
            end_days = 6 - today.weekday()
        elif this_or_next == "next":
            start_days = 7 - today.weekday()
            end_days = start_days + 6
    elif week_or_month == "month":
        if this_or_next == "this":
            start_days = 0
            next_month = (today.month % 12) + 1
            end_days = (datetime(today.year, next_month, 1) - timedelta(days=1)).day - today.day
        elif this_or_next == "next":
            first_day_next_month = datetime(today.year, (today.month % 12) + 1, 1)
            start_days = (first_day_next_month - today).days
            next_month = (first_day_next_month.month % 12) + 1
            end_days = start_days + (datetime(first_day_next_month.year, next_month, 1) - timedelta(days=1)).day - 1

    return start_days, end_days
