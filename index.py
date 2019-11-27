#!/usr/bin/env python3
import webbrowser
import sys
from datetime import date
import time
import os
# pip3 install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# ZOOM_MEETING_URL = "https://zoom.us/j/941904988?pwd=WitDeDZsbFljWlozdy9STVkyMEpYUT09"
ZOOM_FOLDER_PATH = "/home/carlos/Dropbox/Zoom"
# We want to have access to this file to end the observer

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive']
DRIVE_FOLDER_ID = "1IXD1-97R42F5Vz_bBK_47c8_JVuBTP-Y"


def open_zoom_meeting(url):
    """Opens default browser with zoom link, as you would do clicking on the google calendar link"""
    webbrowser.open(url)


def get_folder_name(folder_path):
    return folder_path.split("/")[-1]


def check_new_folder_to_be_zoom_video(folder_name):
    """
    I just check for folders that begin with todays date ...
    2019-11-19 12.57.49 Fiyin Adebayo and carlos loureda parrado 917893445
    """
    return folder_name.startswith(str(date.today()))


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


def upload_to_google_drive(src_folder, parent_folder_id):
    service = login_google_drive()

    # search for folders in google drive
    children = service.files().list(
        q="'" + parent_folder_id + "' in parents",
        spaces='drive',
    ).execute()

    if children:
        files_in_folder = children["files"]
        dest_folder_id = None
        student_name = get_student_name(src_folder)
        # Search for folder for student, if not existant, create it
        for folder in files_in_folder:
            if student_name == folder["name"]:
                dest_folder_id = folder["id"]
                break
        if not dest_folder_id:
            file_metadata = {
                'name': student_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]
            }
            file = service.files().create(body=file_metadata,
                                          fields='id').execute()
            dest_folder_id = file.get('id')
            print(
                f'> Creating folder: {student_name} inside folder: {parent_folder_id}')
        # Create folder for todays call inside student fodler and upload .mp4 file
        if dest_folder_id:
            # TODO: get new folder name
            # TODO: improve to upload eveything besides the mp4

            sub_folder = src_folder[len(ZOOM_FOLDER_PATH)+1:]
            print(
                f'> Creating folder: {sub_folder} inside folder: {dest_folder_id}')
            file_metadata = {
                'name': sub_folder,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [dest_folder_id]
            }
            file = service.files().create(body=file_metadata,
                                          fields='id').execute()
            dest_folder_id = file.get('id')

            file_metadata = {
                'name': 'zoom_0.mp4',
                'parents': [dest_folder_id]
            }
            media = MediaFileUpload(src_folder+"/zoom_0.mp4",
                                    mimetype='video/mp4')
            file = service.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()
            fileId = file.get('id')
            # Grant permission
            try:
                permission = service.permissions().create(
                    fileId=fileId,
                    body={
                        "role": 'reader',
                        "type": 'anyone'
                    }
                )
                webViewLink = service.files().get(
                    fileId=file.get('id'),
                    fields="webViewLink"
                ).execute()

                print('Sharable Link:', webViewLink)
                return webViewLink
            except HttpError as error:
                print('An error occurred: %s' % error)

        # upload to that folder
        # return the link for sharing to the video mp4


class MyHandler(FileSystemEventHandler):
    """Handler needed to manage file changes in our folder """
    @staticmethod
    def on_any_event(event):
        if True:
            if event.event_type == 'moved':
                if event.dest_path.endswith(".mp4"):
                    video_file = event.dest_path
                    folder_path = video_file[0: video_file.find("zoom_0.mp4")]
                    print("-> Video recorded at folder_path: ", folder_path)
                    sharable_link = upload_to_google_drive(
                        folder_path, DRIVE_FOLDER_ID)

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


def main():
    if len(sys.argv) < 2:
        print(">> Please pass the url for the zoom meeting as parameter")
    elif not drive_credentials_exist():
        print(">> I couldn't find a credentials.json file with Google Drive API, please see README.md")
    else:
        zoom_url = sys.argv[1]
        open_zoom_meeting(zoom_url)
        listen_for_call_end()
        # upload_to_google_drive("", "")


if __name__ == "__main__":
    main()
