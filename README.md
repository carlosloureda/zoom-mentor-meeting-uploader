# zoom-mentor-meeting-uploader

A quick Python/Script to upload a zoom meeting to Google Drive to the proper folder and open the submission Google Form for the Nanodegree mentors at Udacity

**DISCLAIMER!** This script is being used on Ubuntu 18.04 with Google Chrome, also tested with Firefox. There is code for executing it on Windows/MacOS but hasn't been tested yet, so use it carefully

## Installation & Requirements

For running this script you need to have `Python 3` & `pip` installed.

There are other packages that need to be installed. Let's see the packages needed:

- watchdog:
  `pip install watchdog`

- Install selenium: pip3 install selenium

  - And drivers: https://selenium-python.readthedocs.io/installation.html#introduction

- Google Drive Python API:
  `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

To register your script in your Google Drive API go to https://developers.google.com/drive/api/v3/quickstart/python:

1.  Turn on the Drive API
    ![turn_on_api]("./img/1_google_drive.png")

2.  Download the crendetials file (`credentials.json`) and save into the working directory of this script

## Configuration

**AUTO-CONFIG** On every script run, it will check this constants for you and will ask for them over the CLI.
The unique thing that you need to provide by yourself is the `crendentials.json` we mentioned above

But you can take a look to `lib/config.json` file and see all the constants need for having the script configured

```json
{
  "selenium": {
    "os": "",
    "browser": "",
    "version": "",
    "bits": "",
    "webdriver_name": "",
    "webdriver_in_filesystem":
  },
  "constants": {
    "ZOOM_FOLDER_PATH": "",
    "DRIVE_FOLDER_ID": "",
    "GOOGLE_FORM_URL": "",
    "MENTOR_EMAIL": ""
  }
}

```

- `ZOOM_FOLDER_PATH` -> Set the folder where Zoom downloads the recorded videos. eg: "/home/carlos/Videos/Zoom"
- `DRIVE_FOLDER_ID` --> Go to Folder of Google Drive and copy FolderID (last part of the url) where you want to store video files
- `GOOGLE_FORM_URL` --> Set the ULR for the google form to upload after each call
- `MENTOR_EMAIL' --> Set your mentor email so selenium will populate it for you on the Google Form

## How it works

**1. Start the script**

`python3 index.js`
or
`python3 index.js https://zoom.us/j/{meetingId}?pwd={password} {student_email}`

If you don't provide the params, CLI will ask for both `zoom_url` and `student_email`.
Also will run all the checks for config files before running

**2. Script will launch Zoom app (opening first the URL on your default browser) and will be listening for the final record to end (will listen for folder cration, and for a .mp4 file created).**

While the recording is begin processed the .mp4 file has the .tmp extension so we wait until the file is created.
We will be using watchdog so you will need to install it.
Also need to set the ZOOM_FOLDER_PATH to know where to listen for.

- We will listen for the "moved" event as it is the event fired when the mp4 file is renamed
- The script will print the final folder when the recording is finished rendering

**3. Upload folder to Drive**

- You need the API_KEY for drive and the Google API Key
  - If there is a folder for that student (_checks for the student name_), the script will upload the folder to that folder
- You need to have the folder for zoom meeting apps created and pass it to the script:
  - If there isn't a folder for that student.

**4. Get the sharable Link for the mp4 video**

Gets the sharable link for the .mp4 file so we can paste it on the google forms.

**5. Moves local file in zoom folder into "students" folder**

**6. Creates a file (if not exists) called `calls_info_{today_date}` appending student email and link**

**7. Fill google forms**

Will fill the first 4 fields of the form: _mentor_email_, _recording_date_, _link_to_video_, _student_email_

I made a little video to explain how it works on [Youtube](https://youtu.be/to_vQ0ZzSlw)

## KNOWN ISSUES

1. After the script ends, and we close the google forms window, the script doesn't finish by itself, so we need to kill it (Ctrl + C)

## To improve

- Don't count on google drive binned files
- Video tutorial

## TO DO

- Fix end of script
- Refactor and improve code

## How to Contribute

Testing on other environments would be much appreciated, you can leave bugs or features suggestions on the **issues** panel of this repo and of course **pull requests** are welcome!
