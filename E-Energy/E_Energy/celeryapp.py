import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_Energy.settings')


app = Celery('E_Energy')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'every-minute': {
        'task': 'app.tasks.records_caching',
        'schedule': crontab(minute='*/1', hour='*/1')
    },
}
