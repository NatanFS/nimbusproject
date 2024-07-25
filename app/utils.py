from datetime import datetime

def format_date(date_str):
    date_formats = [
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%d-%m-%Y %H:%M",
        "%d/%m/%Y %H:%M"
    ]
    
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format).strftime("%d/%m/%Y às %Hh%M")
        except ValueError:
            continue

    return date_str
