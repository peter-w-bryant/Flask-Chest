import json
import logging
import sqlite3
import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from .base import FlaskChestExporter


class FlaskChestExporterInfluxDB(FlaskChestExporter):
    def __init__(
        self,
        app,
        host="localhost",
        port=8086,
        token="",
        org="my-org",
        bucket="my-bucket",
        interval_minutes=1,
    ):
        super().__init__(app, interval_minutes=interval_minutes)
        self.client = InfluxDBClient(
            url=f"http://{host}:{port}",
            token=token,
            org=org,
            debug=False,
        )
        self.org = org
        self.bucket = bucket
        self.start_export_task()

    def export_data(self):
        data = self.fetch_data_from_flask_chest()
        self.write_to_influxdb(data)

    def write_to_influxdb(self, data):
        try:
            write_api = self.client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=self.bucket, org=self.org, record=data)
            logging.info("Data successfully written to InfluxDB")

        except Exception as e:
            logging.error(f"Error writing data to InfluxDB: {e}")

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
                    "time": int(time.time() * 1e9),
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
