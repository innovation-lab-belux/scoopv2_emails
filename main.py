import schedule
import time

def weekly_task():
    print("Weekly task is running!")

# Schedule the task to run every Monday at 9:00 AM
schedule.every().sunday.at("08:00").do(weekly_task)

while True:
    schedule.run_pending()
    time.sleep(1)