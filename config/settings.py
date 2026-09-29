from pathlib import Path
import os

import yaml
from dotenv import load_dotenv


# Project root directory
ROOT_DIR = Path(__file__).resolve().parents[1]

# Load .env
load_dotenv(ROOT_DIR / ".env")


class Settings:

    def __init__(self, environment="lab1"):

        self.environment = environment

        config_file = (
            ROOT_DIR
            / "config"
            / "environments"
            / f"{environment}.yaml"
        )

        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}"
            )

        with open(config_file, "r", encoding="utf-8") as file:
            self.data = yaml.safe_load(file)

    @property
    def base_url(self):
        return self.data["application"]["base_url"]

    @property
    def landing_page(self):
        return self.data["application"]["landing_page"]

    @property
    def login_url(self):
        return (
            self.data["api"]["base_url"]
            + self.data["api"]["login_endpoint"]
        )

    @property
    def username(self):
        return os.getenv("VFST_USERNAME")

    @property
    def password(self):
        return os.getenv("VFST_PASSWORD")

    @property
    def browser_config(self):
        return self.data["browser"]

    @property
    def timeouts(self):
        return self.data["timeouts"]

    @property
    def open_so_details_url(self):
     return (
        self.data["api"]["base_url"]
        + self.data["api"]["open_so_details_endpoint"]
      )