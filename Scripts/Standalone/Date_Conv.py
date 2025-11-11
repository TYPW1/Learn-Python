# convert a date string to DOY and target path
from datetime import datetime

def target_path(dstr):
    # 1. Parse the input string into a real "datetime" object
    # %Y = 4 digit year (2023)
    # %m = 2 digit month (01 - 12)
    # %d = 2 digit day (01 - 31)
    # %H = 2 digit hour (00 - 23)
    dt = datetime.strptime(dstr, "%Y%m%d%H")

    # 2. Use the datetime object to format a new string
    # dt.year:04d -> a 4 digit padded year (2023)
    # dt.strftime ('%j') -> date of year (001 - 366)
    return f"/{dt.year:04d}/{dt.strftime('%j')}"

print (target_path("2024120603")) # -> /2024/341