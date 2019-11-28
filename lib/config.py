import os
import json
import sys
import lib.cli as cli

config_file_path = './lib/config.json'
PATH = "./lib7"


def _check_selenium(config):
    params = None
    if (config["selenium"]["webdriver_name"] == "") or not os.path.exists(config["selenium"]["webdriver_name"]):
        # launch selenium configuration CLI
        print("- Selenium Webdriver missing in config or in folder:")
        params = cli.check_and_download_webdriver()
        # print("params: ", params)

        config["selenium"] = {
            "os": params["os"],
            "browser": params["browser"],
            "version": params["version"],
            "bits": params["bits"] if "bits" in params else "",
            "webdriver_name": params["webdriver_name"],
            "webdriver_in_filesystem": True
        }
        update_config_file(config)


def _check_constants(config):

    if config["constants"]["ZOOM_FOLDER_PATH"] == "":
        answer = cli.ask_for_zoom_folder_path()
        config["constants"]["ZOOM_FOLDER_PATH"] = answer

    if config["constants"]["DRIVE_FOLDER_ID"] == "":
        answer = cli.ask_for_drive_folder_id()
        config["constants"]["DRIVE_FOLDER_ID"] = answer

    if config["constants"]["GOOGLE_FORM_URL"] == "":
        answer = cli.ask_for_google_form_url()
        config["constants"]["GOOGLE_FORM_URL"] = answer

    if config["constants"]["MENTOR_EMAIL"] == "":
        answer = cli.ask_mentor_email()
        config["constants"]["MENTOR_EMAIL"] = answer

    update_config_file(config)


def check_configuration():

    with open(config_file_path) as json_data_file:
        config = json.load(json_data_file)

    _check_selenium(config)
    _check_constants(config)


def update_config_file(new_config):

    with open(config_file_path, 'w') as outfile:
        json.dump(new_config, outfile)


# check_configuration()
