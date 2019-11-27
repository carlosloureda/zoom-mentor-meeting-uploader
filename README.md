# zoom-mentor-meeting-upoader

A quick Python/Script to upload a zoom meeting to Google Drive to the proper folder and open the submission Google Form for the Nanodegree mentors

## About the script

It is going to be coded to be used with Python3 and to be used on Ubuntu folder structure.
Testing on other platforms will be appreciated.

## Installation & Requirements

    - python3
    - pip3
    - watchdog
        - pip install watchdog

    - Add in your index.py the folder where to track the changes for the Zoom apps:
    ZOOM_FOLDER_PATH= "/home/carlos/Videos/Zoom"

    - Google Drive Python API:
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

    - On first attempt you will be prompted the google auth page (unauthorized),
    <!-- TODO: will add some images -->
    Go to Folder of  Google Drive and copy FolderID (last part of the url) and set that value on DRIVE_FOLDER_ID

    - To open Google Form when script ends, set GOOGLE_FORM_URL variable with the google form

    - Install selenium: pip3 install selenium
        - And drivers: https://selenium-python.readthedocs.io/installation.html#introduction

### Get Google Drive API

Go to https://developers.google.com/drive/api/v3/quickstart/python

1. Turn on the Drive API
   ![turn_on_api]("./img/1_google_drive.png")

2. Download the crendetials file (`credentials.json`) and save into the working directory of this script

## How it works

1. Start the script
   `python3 index.js https://zoom.us/j/{meetingId}?pwd={password} {student_email}`

   This will open the default browser as if you where clicking the google calendar link.
   You might need to

2. Once the call begins, the script will be listenning for the final record to end (will listen for folder cration, and for a .mp4 file created)
   While the recording is begin processed the .mp4 file has the .tmp extension so we wait until the file is created.
   We will be using watchdog so you will need to install it.
   Also need to set the ZOOM_FOLDER_PATH to know where to listen for.

   > We will listen for the "moved" event as it is the event fired when the mp4 file is renamed
   > The script will print the final folder when the recorded is finished rendering

3. Upload folder to Drive

   - You need the API_KEY for drive and the Google API Key
   - You need to have the folder for zoom meeting apps created and pass it to the scriptÇ:
     - If there is a folder for that student, the script will upload the folder to that folder
     - If there isn't a folder for that student.
   - It will get the sharable link for the .mp4 file so we can paste it on the google forms

4. Get the sharable Link for the mp4 video

5. Creates a file (if not exists) called `calls_info_{today_date}` appending student email and link

6. Fill google forms
   - Install selenium
   - pass student_email variable as 2nd argument
   - Add MENTOR_EMAIL constant

## Ideas for the script

- Move into proper folder in local
- Open Google Forms: - Paste the url
- Add the date for the video recorded
  - Now you only need to answer the questions and submit the project

## To improve

- Don't count on Bin files
- README with more images
- Video tutorial

# TO DO

- Fix end of script
- Refactor and improve code
