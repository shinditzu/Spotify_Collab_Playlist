from datetime import date, timedelta
from earp_cycle_monthly import cycle
import schedule
import time
import calendar
import os
import dotenv

# dotenv.load_dotenv()

def job():
    today = date.today()
    lastday = calendar.monthrange(today.year, today.month)[1]

    if today.day == lastday:
        cycle()
    else:
        print(f"Today is {today}, not the last day of the month. No action taken.")
        cycle(use_debug=True)

#schedule.every(1).day.at("00:05").do(job)
schedule.every(1).minute.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
