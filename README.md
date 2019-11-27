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

## How it works

1. Start the script
   `python3 index.js https://zoom.us/j/{meetingId}?pwd={password}`

   This will open the default browser as if you where clicking the google calendar link.
   You might need to

2. Once the call begins, the script will be listenning for the final record to end (will listen for folder cration, and for a .mp4 file created)
   While the recording is begin processed the .mp4 file has the .tmp extension so we wait until the file is created.
   We will be using watchdog so you will need to install it.
   Also need to set the ZOOM_FOLDER_PATH to know where to listen for.

   > We will listen for the "moved" event as it is the event fired when the mp4 file is renamed
   > The script will print the final folder when the recorded is finished rendering

## Ideas for the script

- Optionally open zoom link
- listen for new Zoom video recorded
- Upload it to gogle Drive (on the proper folder)
- Get url
- Move into proper folder in local
- Open Google Forms: - Paste the url
- Add the date for the video recorded
- Retreive from somwhere
  - student email
  - my email
  - Now you only need to answer the questions and submit the project
