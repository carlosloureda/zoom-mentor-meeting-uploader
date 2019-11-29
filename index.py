#!/usr/bin/env python3
import webbrowser
from datetime import datetime
import sys
import time
import os
# pip3 install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from googleapiclient.http import MediaFileUpload
import google_forms_scapper
import json
import lib.config as config
import lib.google_drive as google_drive
import inquirer

ZOOM_FOLDER_PATH = ""
DRIVE_FOLDER_ID = ""
GOOGLE_FORM_URL = ""
MENTOR_EMAIL = ""

# Global variables
STUDENT_EMAIL = ""


def open_zoom_meeting(url):
    """Opens default browser with zoom link, as you would do clicking on the google calendar link"""
    webbrowser.open(url)


def login_google_drive():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)


def get_student_name(folder):
    """
    From a folder name like this one: /home/carlos/Dropbox/Zoom/2019-11-27 16.21.49 Carlos David Loureda Parrado and carlos loureda parrado 941904988/
    We retrieve the Carlos David Loureda Parrado as folder name
    """
    # TODO: Improve this with regex
    sub_folder = folder[len(ZOOM_FOLDER_PATH):]
    _from = sub_folder.find(" ", 19)  # 19 is the length of the datetime
    _to = sub_folder.find(" and")
    return sub_folder[_from+1: _to]


def save_into_file(student_email, link):
    filename = "calls_info_" + datetime.today().strftime('%m_%d_%Y')
    f = open(filename, "a")
    f.write(f'## Student email: {student_email} \n\t> URL: {link}\n\n')
    f.close()


def move_local_folder(folder_path):
    folder_name = folder_path[len(ZOOM_FOLDER_PATH):]
    username = get_student_name(folder_path)
    files = os.listdir(ZOOM_FOLDER_PATH)
    student_folder = ZOOM_FOLDER_PATH + "/" + username
    if username not in files:
        os.makedirs(student_folder)
    os.rename(folder_path, student_folder+"/"+folder_name)


class MyHandler(FileSystemEventHandler):
    """Handler needed to manage file changes in our folder """
    @staticmethod
    def on_any_event(event):
        # print("event: ", event)
        global STUDENT_EMAIL
        if event.event_type == 'moved':
            # print(">>> MOVED: ", event)
            if event.dest_path.endswith(".mp4"):
                video_file = event.dest_path
                folder_path = video_file[0: video_file.find("zoom_0.mp4")]
                print("-> Video recorded at folder_path: ", folder_path)
                sharable_link = google_drive.upload_to_google_drive(
                    folder_path, DRIVE_FOLDER_ID, ZOOM_FOLDER_PATH, get_student_name(folder_path))
                move_local_folder(folder_path)
                save_into_file(STUDENT_EMAIL,
                               sharable_link)
                google_forms_scapper.open_and_fill_form(
                    GOOGLE_FORM_URL,
                    sharable_link,
                    MENTOR_EMAIL,
                    STUDENT_EMAIL)
                print("here we should end observer")
                # TODO: search for a way to close program here
                # raise KeyboardInterrupt

                # 3. move local folder to its own folder
                # 4. End observer


def listen_for_call_end():
    """Once the meeting starts we want to be listening for the meeting to finish and """
    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, ZOOM_FOLDER_PATH, recursive=True)
    observer.start()
    print("File observer started, Interrupt script execution with `Ctrl+C`")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()


def drive_credentials_exist():
    """Checks if credentials.json file exists"""
    return os.path.isfile('./credentials.json')


def get_constants_from_config_file():
    """Initializes constants from config file"""
    global ZOOM_FOLDER_PATH
    global DRIVE_FOLDER_ID
    global GOOGLE_FORM_URL
    global MENTOR_EMAIL
    with open("./lib/config.json") as json_data_file:
        config = json.load(json_data_file)
        ZOOM_FOLDER_PATH = config["constants"]["ZOOM_FOLDER_PATH"]
        DRIVE_FOLDER_ID = config["constants"]["DRIVE_FOLDER_ID"]
        GOOGLE_FORM_URL = config["constants"]["GOOGLE_FORM_URL"]
        MENTOR_EMAIL = config["constants"]["MENTOR_EMAIL"]


def check_and_parse_zoom_url(zoom_url):
    """Checks if we have a proper zoom_url, if it has the google prefix it removes it and shows a proper zoom url"""
    google_url_pref = "https://www.google.com/url?q="
    while True:
        if "https://zoom.us" in zoom_url:
            if google_url_pref in zoom_url:
                zoom_url = zoom_url[len(google_url_pref):]
            break
        else:
            print("[ERROR] Link provided is not an Zoom meeting link")
            questions = [
                inquirer.Text('zoom_url',
                              message="Please a correct zoom url:")
            ]
            zoom_url = inquirer.prompt(questions)["zoom_url"]
    return zoom_url



def main():
    global STUDENT_EMAIL
    zoom_url = ""
    if not drive_credentials_exist():
        print(">> I couldn't find a credentials.json file with Google Drive API, please see README.md")
        return
    if len(sys.argv) < 2:
        answers = {}
        while answers == {} or ("zoom_url" in answers and answers["zoom_url"] == ""):
            questions = [
                inquirer.Text('zoom_url',
                              message="Please paste the zoom url for this call")
            ]
            answers = inquirer.prompt(questions)
            zoom_url = check_and_parse_zoom_url(answers["zoom_url"])
        questions = [
            inquirer.Text('student_email',
                          message="Please add student email")
        ]
        answers = inquirer.prompt(questions)
        STUDENT_EMAIL = answers["student_email"] if "student_email" in answers else ""
    else:
        zoom_url = check_and_parse_zoom_url(sys.argv[1])
        STUDENT_EMAIL = sys.argv[2]
    get_constants_from_config_file()
    config.check_configuration()
    open_zoom_meeting(zoom_url)
    listen_for_call_end()


if __name__ == "__main__":
    main()
