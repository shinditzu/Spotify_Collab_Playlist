from datetime import date, timedelta, datetime
from spotify_tools import cycle
import schedule
import time
import calendar
import os
import dotenv
import pytz

# dotenv.load_dotenv()
print("Starting Spotify Cycle Service...")

tz = pytz.timezone("America/New_York")
today = date.today()
lastday_num = calendar.monthrange(today.year, today.month)[1]
lastday = date(today.year, today.month, lastday_num)
firstday = date(today.year, today.month, 1)
current_time = time.localtime()

def job():
    now = datetime.now(tz)
    today = now.date()

    print(f"Job running at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")


    if today == firstday:
        print(f"Today is {today} time is {now.strftime('%H:%M')}, the first day of the month. I just cycled the live playlist.")
        cycle(use_debug=False, write_csv=False)

    elif today == lastday:
        print(f"Today is {today} time is {now.strftime('%H:%M')}, the last day of the month. I'm going to cycle the live list tomorrow.")
        cycle(use_debug=True)
    else:
        print(f"Today is {today} time is {now.strftime('%H:%M')}, not the last day of the month. Running debug flow.")
        cycle(use_debug=True,write_csv=False)

schedule.every(1).day.at("00:05", str(tz)).do(job)
#schedule.every(1).minute.do(job)

while True:
    print(f"{datetime.now(tz).strftime('%Y-%m-%d %H:%M')}. Checking if it's time to run the job...")
    schedule.run_pending() #check for jobs to run.
    time.sleep(60) #sleep for 60 seconds
