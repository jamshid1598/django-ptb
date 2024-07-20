import os
import dotenv
from pathlib import Path
from celery import Celery
from celery.schedules import crontab


base_dir = Path(__file__).resolve().parent.parent
dotenv.read_dotenv(os.path.join(base_dir, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# Schedule the task to run every minute
# app.conf.beat_schedule = {
#     'fetch-monthly-update': {
#         'task': 'apps.egaz.tasks.update_before_month_data',
#         'schedule': crontab(0, 0, day_of_month='11'), # task runs 11th day of every month to update before month data
#     },
# }
