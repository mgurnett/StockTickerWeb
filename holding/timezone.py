from datetime import datetime as dt
print("Python program to demonstrate strftime() function using datetime module")
now = dt.now()
print("The current date and time without formatting is as follows:")
print(now)
s = now.strftime("%Z %z")
print("This will display the timezone:")
print(s)