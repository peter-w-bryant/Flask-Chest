import logging
import sqlite3
import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from .base import FlaskChestExporter


# The class FlaskChestExporterInfluxDB is a subclass of FlaskChestExporter and is used for exporting
# data to InfluxDB.
class FlaskChestExporterInfluxDB(FlaskChestExporter):
    def __init__(
        self,
        chest,
        host="localhost",
        port=8086,
        token="",
        org="my-org",
        bucket="my-bucket",
        interval_minutes=5,
    ):
        super().__init__(chest, interval_minutes=interval_minutes)
        self.client = InfluxDBClient(
            url=f"http://{host}:{port}",
            token=token,
            org=org,
            debug=False,
        )
        self.chest = chest
        self.org = org
        self.bucket = bucket
        self.start_export_task()

    def export_data(self):
        """
        The function "export_data" is used to export data from flask_chest table to InfluxDB.
        """
        data = self.fetch_data_from_flask_chest()
        self.write_to_influxdb(data)

    def write_to_influxdb(self, data):
        """
        The function "write_to_influxdb" is used to write data to an InfluxDB database.

        :param data: The "data" parameter is the data that you want to write to InfluxDB. It can be in any
        format that InfluxDB supports, such as JSON or line protocol
        """
        try:
            write_api = self.client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=self.bucket, org=self.org, record=data)
            logging.info("Data successfully written to InfluxDB")
            print("Data successfully written to InfluxDB")

        except Exception as e:
            logging.error(f"Error writing data to InfluxDB: {e}")
            print("Error writing data to InfluxDB")

    def fetch_data_from_flask_chest(self):
        """
        The function fetches data from a Flask server related to the chest.
        """
        conn = sqlite3.connect(self.chest.db_uri)
        cursor = conn.cursor()
        query = "SELECT unique_id, request_id, name, value FROM flask_chest"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            influxdb_data = []

            # For each row in flask_chest table, create a data point
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

            # Remove rows from flask_chest table
            cursor.execute("DELETE FROM flask_chest")
            conn.commit()

            return influxdb_data
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in query: {e}")
        finally:
            cursor.close()
            conn.close()
