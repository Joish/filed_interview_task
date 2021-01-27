from datetime import datetime

def get_month_year(date):
    dt = datetime.strptime(date, '%m/%Y')
    month = dt.month
    year = dt.year
    return month,year