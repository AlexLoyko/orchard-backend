from datetime import datetime

def str_to_date(date):
    try:
        return datetime.strptime(date, '%m/%d/%Y')
    except:
        return None

def int_or_none(field):
    try:
        return int(field)
    except:
        return None

def grade_or_none(grade):
    if str(grade) in "ABC":
        return grade
    else:
        return None
