# In your Flask app module
import sqlite3
import subprocess
import sys
import time

from celery.schedules import crontab
from celery_config import make_celery
from flask import Flask
from influxdb import InfluxDBClient


class FlaskChestExporter:
    def __init__(self, app: Flask, interval_minutes: int = 5):
        self.celery = make_celery(app)
        self.interval_minutes = interval_minutes

    def setup_periodic_task(self):
        @self.celery.on_after_configure.connect
        def setup_periodic_tasks(sender, **kwargs):
            sender.add_periodic_task(
                crontab(minute=f"*/{self.interval_minutes}"), self.export_data.s()
            )

        @self.celery.task
        def export_data(self):
            raise NotImplementedError("This method should be implemented by subclass.")


class FlaskChestExporterInfluxDB(FlaskChestExporter):
    def __init__(self, app, host, port, username, password, dbname):
        super().__init__(app)
        self.client = InfluxDBClient(host, port, username, password, dbname)

    def write_to_influxdb(self, data):
        self.client.write_points(data)

    def export_data(self):
        data = self.fetch_data_from_flask_chest()
        self.write_to_influxdb(data)

    def fetch_data_from_flask_chest(self):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        query = "SELECT unique_id, request_id, name, value FROM flask_chest"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            influxdb_data = []
            for row in rows:
                data_point = {
                    "measurement": "sample",
                    "tags": {
                        "unique_id": row[0],
                        "request_id": row[1],
                    },
                    "fields": {
                        "name": row[2],
                        "value": row[3],
                    },
                    "time": time.time(),
                }
                influxdb_data.append(data_point)
            return influxdb_data
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in query: {e}")
        finally:
            cursor.close()
            conn.close()
