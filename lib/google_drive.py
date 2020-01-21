from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import socket
import os
import pickle


SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive']


def login_google_drive():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../token.pickle'):
        with open('../token.pickle', 'rb') as token:
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
        with open('../token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)


def upload_file(service, file_path, mime_type, dest_folder_id):
    """Uploads a file into a destination folder on Google Drive"""
    file_metadata = {
        'mimeType': mime_type,
        'name': 'zoom_0.mp4',
        'parents': [dest_folder_id]
    }
    media = MediaFileUpload(file_path,
                            mimetype=mime_type,
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    return file.get('id')


def create_shareble_link(service, fileId):
    """Makes a file public and returns the url for sharing"""
    try:
        service.permissions().create(
            fileId=fileId,
            body={
                "role": 'reader',
                "type": 'anyone'
            }
        ).execute()
        webViewLink = service.files().get(
            fileId=fileId,
            fields="webViewLink"
        ).execute()

        return webViewLink["webViewLink"]
    except HttpError as error:
        print('An error occurred: %s' % error)
    return None


def create_folder(service, folder_name, parent_id):
    """Creates a folder in google drive"""
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    file = service.files().create(body=file_metadata,
                                  fields='id').execute()
    return file.get('id')


def upload_to_google_drive(src_folder, parent_folder_id, path, student_name):
    """Uploads folder to folder in google_drive"""
    service = login_google_drive()

    # search for folders in google drive
    children = service.files().list(
        q="'" + parent_folder_id + "' in parents",
        spaces='drive',
    ).execute()

    if children:
        files_in_folder = children["files"]
        dest_folder_id = None
        # Search for folder for student, if not existant, create it
        for folder in files_in_folder:
            if student_name == folder["name"]:
                dest_folder_id = folder["id"]
                break
        if not dest_folder_id:
            dest_folder_id = create_folder(
                service, student_name, parent_folder_id)
            print(
                f'> Creating folder: {student_name} inside folder: {parent_folder_id}')
        # Create folder for todays call inside student fodler and upload .mp4 file
        if dest_folder_id:
            # sub_folder = src_folder[len(path)+1:]
            sub_folder = src_folder[src_folder.find('//')+2:]
            print(
                f'> Creating folder: {sub_folder} inside folder: {dest_folder_id}')
            dest_folder_id = create_folder(service, sub_folder, dest_folder_id)

            # UPLOAD FOLDER
            file = src_folder + "/zoom_0.mp4"
            fileId = upload_file(service, file, 'video/mp4', dest_folder_id)

            # Grant permission
            return create_shareble_link(service, fileId)

    return None


# service = login_google_drive()
# fileId = upload_file(service, "/home/carlos/Dropbox/Zoom/2019-11-28 17.48.45 carlos loureda parrado's Zoom Meeting 237965513/zoom_0.mp4", "video/mp4",
#                      "1IXD1-97R42F5Vz_bBK_47c8_JVuBTP-Y")
# url = create_shareble_link(service, fileId)
# print("URL: ", url)

# ZOOM_FOLDER_PATH
