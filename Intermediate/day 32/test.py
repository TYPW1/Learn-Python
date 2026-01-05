# import smtplib
# my_email = "pierretypw@gmail.com"
# password = input("Type your password and press enter: ")

# connection = smtplib.SMTP("smtp.gmail.com")
# connection.starttls()
# connection.login(my_email, password)
# connection.sendmail(
#     from_addr=my_email,
#     to_addrs="wilfried.titcheuyamdjeu@uni.lu",
#     msg="Subject: Test Email\n\nThis is a test email."
# )
# connection.close()

import datetime as dt
now = dt.datetime.now()
date_of_birth = dt.datetime(year=1997, month=10, day=15, hour=23, minute=30, second=59)
print(date_of_birth)

string_test = "Hello"
print(string_test.split("l"))