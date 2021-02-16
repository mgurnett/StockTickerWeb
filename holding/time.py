import datetime

TIMESTAMP_FORMAT = "%a, %e %b %Y - %l:%M %p"

print (datetime.datetime.now().strftime(TIMESTAMP_FORMAT))