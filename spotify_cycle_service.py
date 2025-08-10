from datetime import date, timedelta
from earp_cycle_monthly import cycle
import schedule
import time
import calendar
import os
import dotenv

# dotenv.load_dotenv()

today = date.today()
lastday_num = calendar.monthrange(today.year, today.month)[1]
lastday = date(today.year, today.month, lastday_num)
firstday = date(today.year, today.month, 1)

def job():
    if today == firstday:
        print(f"Today is {today}, the first day of the month. I just cycled the live playlist.")
        cycle(use_debug=False)

    elif today == lastday:
        print(f"Today is {today}, the last day of the month. I'm going to cycle the live list tomorrow.")
        cycle(use_debug=True)
    else:
        print(f"Today is {today}, not the last day of the month. Running debug flow.")
        cycle(use_debug=True)

schedule.every(1).day.at("00:05").do(job)
# schedule.every(1).minute.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
