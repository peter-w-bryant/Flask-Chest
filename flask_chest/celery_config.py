# celery_config.py
from celery import Celery


def make_celery(app):
    # Configure Celery, using Redis as the broker
    celery = Celery(app.import_name, broker='redis://localhost:6379/0')

    # Run Celery in the Flask application context
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
