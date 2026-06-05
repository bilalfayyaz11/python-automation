#!/usr/bin/env python3
"""
Manufacturing Equipment Simulator
Generates realistic telemetry data for production machines.
"""

import os
import time
import random
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class EquipmentSimulator:
    def __init__(self, equipment_id, equipment_type):
        self.equipment_id = equipment_id
        self.equipment_type = equipment_type

        self.url = os.getenv("INFLUX_URL", "http://localhost:8086")
        self.token = os.getenv("INFLUX_TOKEN", "manufacturing-token-123")
        self.org = os.getenv("INFLUX_ORG", "manufacturing-org")
        self.bucket = os.getenv("INFLUX_BUCKET", "manufacturing")

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org
        )

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def generate_telemetry(self):
        if random.random() < 0.05:
            status = "error"
            speed = 0
        elif random.random() < 0.15:
            status = "idle"
            speed = random.randint(0, 20)
        else:
            status = "error"
            speed = 0
            speed = random.randint(60, 100)

        return {
            "temperature": round(random.uniform(60, 95), 2),
            "pressure": round(random.uniform(20, 50), 2),
            "speed": speed,
            "status": status,
            "timestamp": datetime.now(timezone.utc)
        }

    def send_telemetry(self, telemetry_data):
        point = (
            Point("equipment_metrics")
            .tag("equipment_id", self.equipment_id)
            .tag("equipment_type", self.equipment_type)
            .field("temperature", telemetry_data["temperature"])
            .field("pressure", telemetry_data["pressure"])
            .field("speed", telemetry_data["speed"])
            .field("status", telemetry_data["status"])
            .time(telemetry_data["timestamp"])
        )

        self.write_api.write(
            bucket=self.bucket,
            org=self.org,
            record=point
        )

    def run(self, duration=60):
        start_time = time.time()

        print(f"Starting simulator for {self.equipment_id} ({self.equipment_type})")

        while time.time() - start_time < duration:
            telemetry = self.generate_telemetry()
            self.send_telemetry(telemetry)

            print(
                f"{telemetry['timestamp'].isoformat()} | "
                f"{self.equipment_id} | "
                f"temp={telemetry['temperature']}C | "
                f"pressure={telemetry['pressure']}PSI | "
                f"speed={telemetry['speed']}% | "
                f"status={telemetry['status']}"
            )

            time.sleep(5)

        print("Simulation complete.")


if __name__ == "__main__":
    simulator = EquipmentSimulator("MACHINE-001", "CNC_MILL")
    simulator.run(duration=60)
