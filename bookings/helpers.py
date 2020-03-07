from datetime import datetime, timedelta
import uuid

def to_date(str_date):
    format_date = '%Y-%m-%d'
    _date = datetime.strptime(str_date, format_date)
    return _date.date()

def diff_dates(start_date, end_date):
    return (end_date - start_date).days + 1

def generate_locator():
    return uuid.uuid4().hex[:10].upper()