import re
from pytz import timezone
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import os

TZ = timezone("Europe/Kiev")
DB_DSN = os.environ.get("DB_DSN", "")
TG_TOKEN = os.environ.get("TG_TOKEN", "")
GENDER, CARD_NUMBER, CVV = range(3)
RSS_URL = SETTINGS = 0

URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
CANCEL_REGEX = re.compile(r'/cancel')

executors = {'default': ThreadPoolExecutor(10)}
jobstores = {"default": SQLAlchemyJobStore(url=DB_DSN, tablename="apscheduler")}
scheduler = BackgroundScheduler(jobstores=jobstores, timezone=TZ)
