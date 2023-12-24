# In your Flask app module
import subprocess

from celery.schedules import crontab
from celery_config import make_celery
from flask import Flask

app = Flask(__name__)
celery = make_celery(app)

class FlaskChestExporter:
    def __init__(self, app: Flask, script_path: str, interval_minutes: int = 5):
        self.celery = make_celery(app)
        self.script_path = script_path
        self.interval_minutes = interval_minutes
        self.setup_periodic_task()

    def setup_periodic_task(self):
        @celery.on_after_configure.connect
        def setup_periodic_tasks(sender, **kwargs):
            sender.add_periodic_task(
                crontab(minute=f'*/{self.interval_minutes}'),
                self.run_script.s()
            )

        @self.celery.task
        def run_script(self):
            subprocess.run(['python', self.script_path])