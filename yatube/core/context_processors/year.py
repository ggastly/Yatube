import datetime as dt


def year(request):
    now = dt.date.today()
    year = now.year
    return {
        'year': year,
    }
