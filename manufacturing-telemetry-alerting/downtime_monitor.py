#!/usr/bin/env python3

import os
import time
from datetime import datetime
from influxdb_client import InfluxDBClient


class DowntimeMonitor:

    def __init__(self, check_interval=10):

        self.check_interval = check_interval
        self.downtime_threshold = 30

        self.url = os.getenv("INFLUX_URL", "http://localhost:8086")
        self.token = os.getenv("INFLUX_TOKEN", "manufacturing-token-123")
        self.org = os.getenv("INFLUX_ORG", "manufacturing-org")
        self.bucket = os.getenv("INFLUX_BUCKET", "manufacturing")

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )

        self.query_api = self.client.query_api()

        self.alert_cooldown = {}

    def query_equipment_status(self, equipment_id):

        query = f'''
from(bucket: "{self.bucket}")
  |> range(start: -2m)
  |> filter(fn: (r) => r["_measurement"] == "equipment_metrics")
  |> filter(fn: (r) => r["equipment_id"] == "{equipment_id}")
  |> filter(fn: (r) => r["_field"] == "status")
  |> last()
'''

        result = self.query_api.query(org=self.org, query=query)

        statuses = []

        for table in result:
            for record in table.records:
                statuses.append(record.get_value())

        return statuses

    def detect_downtime(self, equipment_id):

        statuses = self.query_equipment_status(equipment_id)

        if not statuses:
            return True, "No telemetry received"

        latest_status = statuses[-1]

        if latest_status == "error":
            return True, "Equipment reporting error state"

        return False, "Operating normally"

    def send_alert(self, equipment_id, reason):

        current_time = time.time()

        if equipment_id in self.alert_cooldown:
            last_alert = self.alert_cooldown[equipment_id]

            if current_time - last_alert < 300:
                return

        self.alert_cooldown[equipment_id] = current_time

        alert_message = (
            f"{datetime.utcnow().isoformat()} | "
            f"{equipment_id} | "
            f"{reason}\n"
        )

        with open("/tmp/manufacturing_alerts.log", "a") as file:
            file.write(alert_message)

        print(f"ALERT: {alert_message.strip()}")

    def monitor(self, equipment_list):

        print("Starting downtime monitor...")

        while True:

            for equipment in equipment_list:

                is_down, reason = self.detect_downtime(equipment)

                if is_down:
                    self.send_alert(equipment, reason)

            time.sleep(self.check_interval)


if __name__ == "__main__":

    monitor = DowntimeMonitor(check_interval=10)

    equipment_to_monitor = [
        "MACHINE-001",
        "MACHINE-002"
    ]

    monitor.monitor(equipment_to_monitor)
