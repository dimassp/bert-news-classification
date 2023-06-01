from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from job.tasks2 import scrape_and_classify

trigger = OrTrigger([CronTrigger(hour=22,minute=10), CronTrigger(hour=12,minute=30)])

scheduler = BackgroundScheduler()

# scheduler.add_job(print_name,trigger)