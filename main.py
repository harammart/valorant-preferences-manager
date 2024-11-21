import json
import os
import sys
import logging

import urllib3
from rich.prompt import Prompt
from rich.logging import RichHandler

import valorant
import constants

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

def main():
    if not os.path.exists(constants.lock_file_path):
        log.critical("It looks like Riot Client isn't running. Please launch it and try again.")
        sys.exit(1)

    os.makedirs(constants.profile_path, exist_ok=True)

    val = valorant.ValorantInternal()

    choice = Prompt.ask("Select the task you want to perform", choices=["save", "load"], default="save", case_sensitive=False)
    if choice == "save":
        preferences = val.get_preferences()
        profile_name = Prompt.ask("Name of the profile")
        with open(f"profiles/{profile_name}.json", "w") as profile:
            json.dump(preferences, profile)
    elif choice == "load":
        profile_name = Prompt.ask("Name of the profile")
        with open(f"profiles/{profile_name}.json", "r") as profile:
            profile = json.load(profile)
            result = val.set_preferences(profile)
            log.info(f"Set preferences result: {result}")

if __name__ == '__main__':
    main()