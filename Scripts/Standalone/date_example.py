from datetime import datetime, timedelta

# Get the current date and time
now = datetime.now()
print(f"Current time is: {now}")

one_day = timedelta(days=1)
yesterday = now - one_day
print(f"Yesterday was: {yesterday}")

print(f"Formatted date: {now.strftime('%Y-%m-%d %H:%M:%S')}")