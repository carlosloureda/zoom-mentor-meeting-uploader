# check for installed modules

# pip3 install watchdog
# googleapiclient

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import zipfile
import urllib.request
import subprocess
import sys
import os
from pprint import pprint
# sys.path.append(os.path.abspath(os.path.join('..', 'utils')))
# try:
# from utils.loading_animation import Animation
import lib.loading_animations as loading_animations
# except e:
#     print("algo pasó: ", e)
#     pass

# Required python and pip


def install(package):
    """Installs a package from command line"""
    subprocess.call([sys.executable, "-m", "pip", "install", package])


try:
    import inquirer
except ImportError:
    install("inquirer")
    import inquirer


def checkand_download_modules():
    print(">> Checking for required modules")
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    required_packages = ["watchdog", "google-api-python-client",
                         "google-auth-httplib2", "google-auth-oauthlib", "selenium", "inquirer", "pprint"]

    for package in required_packages:
        if not package in installed_packages:
            install(package)


def ask_for_zoom_folder_path():
    questions = [
        inquirer.Text('ZOOM_FOLDER_PATH',
                      message="Please add the zoom folder path")
    ]
    answers = inquirer.prompt(questions)
    return answers["ZOOM_FOLDER_PATH"]


def ask_for_drive_folder_id():
    questions = [
        inquirer.Text('DRIVE_FOLDER_ID',
                      message="Add ID of google drive folder to upload videos")
    ]
    answers = inquirer.prompt(questions)
    return answers["DRIVE_FOLDER_ID"]


def ask_for_google_form_url():
    questions = [
        inquirer.Text('GOOGLE_FORM_URL',
                      message="Add URl for Google Forms")
    ]
    answers = inquirer.prompt(questions)
    return answers["GOOGLE_FORM_URL"]


def ask_mentor_email():
    questions = [
        inquirer.Text('MENTOR_EMAIL',
                      message="Add your mentor email")
    ]
    answers = inquirer.prompt(questions)
    return answers["MENTOR_EMAIL"]


def check_and_download_webdriver():
    files_urls = {
        # Safair doesnt need webdriver: https://webkit.org/blog/6900/webdriver-support-in-safari-10/
        "Chrome": {
            "77": {
                "Linux": "https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip",
                "Mac": "https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_mac64.zip",
                "Windows": "https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_win32.zip"
            },
            "78": {
                "Linux": "https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_linux64.zip",
                "Mac": "https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_mac64.zip",
                "Windows": "https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_win32.zip"
            },
            "79": {
                "Linux": "https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip",
                "Mac": "https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_mac64.zip",
                "Windows": "https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_win32.zip"
            }
        },
        "Edge": {
            "75": {
                "32": "https://msedgedriver.azureedge.net/75.0.139.20/edgedriver_win32.zip",
                "64": "https://msedgedriver.azureedge.net/75.0.139.20/edgedriver_win64.zip",
            },
            "76": {
                "32": "https://msedgedriver.azureedge.net/76.0.183.0/edgedriver_win32.zip",
                "64": "https://msedgedriver.azureedge.net/76.0.183.0/edgedriver_win64.zip",
            },
            "77": {
                "32": "https://msedgedriver.azureedge.net/77.0.237.0/edgedriver_win32.zip",
                "64": "https://msedgedriver.azureedge.net/77.0.237.0/edgedriver_win64.zip",
            },
            "78": {
                "32": "https://msedgedriver.azureedge.net/78.0.277.0/edgedriver_win32.zip",
                "64": "https://msedgedriver.azureedge.net/78.0.277.0/edgedriver_win64.zip",
            },
            "79": {
                "32": "https://msedgedriver.azureedge.net/79.0.313.0/edgedriver_win32.zip",
                "64": "https://msedgedriver.azureedge.net/79.0.313.0/edgedriver_win64.zip",
            },
            "80": {
                "32": "https://msedgedriver.azureedge.net/80.0.346.0/edgedriver_win32.zip",
                "64": "https://msedgedriver.azureedge.net/80.0.346.0/edgedriver_win64.zip",
            }
        },
        "Firefox": {
            ">=60": {
                "Linux": {
                    "32": "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux32.tar.gz",
                    "64": "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz"
                },
                "Mac": {
                    # TOOD: are the same
                    "32": "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-macos.tar.gz",
                    "64": "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-macos.tar.gz",
                },
                "Windows": {
                    "32": "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win32.zip",
                    "64": "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip"
                }
            }
        }

    }
    questions = [
        inquirer.List('browser',
                      message="What browser do you use?",
                      choices=['Chrome', 'Firefox', 'Edge', 'Safari'],
                      ),
        inquirer.List('os',
                      message="What operative system do you use?",
                      choices=['Linux', 'Mac', 'Windows'],
                      ),
    ]

    answers = inquirer.prompt(questions)
    if answers["browser"] == "Chrome":
        questions = [
            inquirer.List('version',
                          message="What version of Chrome?",
                          choices=['77', '78', '79'],
                          ),
        ]
        answers.update(inquirer.prompt(questions))
    elif answers["browser"] == "Firefox":
        questions = [
            inquirer.List('version',
                          message="What version of Firefox?",
                          choices=['>=60'],
                          ),
            inquirer.List('bits',
                          message="32bits or 64 bits?",
                          choices=['32', '64'],
                          ),
        ]
        answers.update(inquirer.prompt(questions))
    elif answers["browser"] == "Edge":
        questions = [
            inquirer.List('version',
                          message="What version of Edge?",
                          choices=['75', '76', '77', '78', '79', '80'],
                          ),
            inquirer.List('bits',
                          message="Windows 32bits or 64 bits?",
                          choices=['32', '64'],
                          ),

        ]
        answers.update(inquirer.prompt(questions))
    if answers["browser"] != "Safari":
        prev_url = files_urls[answers["browser"]][answers["version"]]
    url = None
    if answers["browser"] == "Edge":
        url = prev_url[answers["bits"]]
    elif answers["browser"] == "Firefox":
        url = prev_url[answers["os"]][answers["bits"]]
    elif answers["browser"] == "Chrome":
        url = prev_url[answers["os"]]

    # Download zip file
    url_splitted = url.split("/")

    file_name = url_splitted[len(url_splitted)-1]
    animation = loading_animations.Animation("Downloading webdriver: " + file_name,
                                             "Finished Downloading webdriver!")
    animation.start()

    urllib.request.urlretrieve(url, file_name)
    animation.stop()

    # Extract zip file
    animation = loading_animations.Animation("Uncompressing webdriver",
                                             "Finished uncompression of webdriver!")
    animation.start()

    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall("./")
        os.remove(file_name)
        animation.stop()

        answers["webdriver_name"] = zip_ref.namelist()[0]
    return answers
    # print("uncompressing ...")
    # zipfile = ZipFile(BytesIO(resp.read()))
    # zipfile.namelist()


# checkand_download_modules()
# check_and_download_webdriver()
# check constants config

# Download and unzip
# Save config in file
