#!/usr/bin/env python3
import os
import json
from datetime import datetime
from typing import Optional


class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        os.makedirs(self.config_dir, exist_ok=True)
        self.current_config_file = os.path.join(config_dir, "active_profile.json")

    def set_active_profile(self, profile_name: str) -> None:
        payload = {
            "active_profile": profile_name,
            "switched_at": datetime.utcnow().isoformat() + "Z"
        }

        with open(self.current_config_file, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

    def get_active_profile(self) -> Optional[str]:
        if not os.path.exists(self.current_config_file):
            return None

        with open(self.current_config_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get("active_profile")

    def list_available_profiles(self) -> list:
        profiles_dir = os.path.join(self.config_dir, "profiles")
        if not os.path.isdir(profiles_dir):
            return []

        return sorted(
            filename.replace(".yaml", "")
            for filename in os.listdir(profiles_dir)
            if filename.endswith(".yaml")
        )

    def profile_exists(self, profile_name: str) -> bool:
        return profile_name in self.list_available_profiles()
