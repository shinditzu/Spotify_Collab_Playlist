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

def job():
    now = datetime.now(tz)
    today = now.date()
    
    # Calculate first and last day of current month
    firstday = date(today.year, today.month, 1)
    lastday_num = calendar.monthrange(today.year, today.month)[1]
    lastday = date(today.year, today.month, lastday_num)

    print(f"Job running at {now.strftime('%Y-%m-%d %H:%M:%S')}")


    if today == firstday:
        print(f"Today is {today} time is {now.strftime('%H:%M')}, the first day of the month. I just cycled the live playlist.")
        cycle(use_debug=False, write_csv=True)

    elif today == lastday:
        print(f"Today is {today} time is {now.strftime('%H:%M')}, the last day of the month. I'm going to cycle the live list tomorrow.")
        cycle(use_debug=True)
    else:
        print(f"Today is {today} time is {now.strftime('%H:%M')}, not the last day of the month. Running debug flow.")
        cycle(use_debug=True,write_csv=False)

schedule.every(1).day.at("00:15", str(tz)).do(job)
#schedule.every(1).minute.do(job)

while True:
    current_now = datetime.now(tz)
    current_today = current_now.date()
    current_firstday = date(current_today.year, current_today.month, 1)
    current_lastday_num = calendar.monthrange(current_today.year, current_today.month)[1]
    current_lastday = date(current_today.year, current_today.month, current_lastday_num)
    
    print(f"{current_now.strftime('%Y-%m-%d %H:%M')}. Checking if it's time to run the job...")
    print(f"today is {current_today}, lastday is {current_lastday}, firstday is {current_firstday}, current time is {current_now.strftime('%H:%M')}")

    schedule.run_pending() #check for jobs to run.
    time.sleep(60) #sleep for 60 seconds



