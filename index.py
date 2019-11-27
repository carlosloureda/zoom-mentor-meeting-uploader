#!/usr/bin/env python3
import webbrowser
import sys
from datetime import date
import time

# pip3 install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ZOOM_MEETING_URL = "https://zoom.us/j/941904988?pwd=WitDeDZsbFljWlozdy9STVkyMEpYUT09"
ZOOM_FOLDER_PATH = "/home/carlos/Dropbox/Zoom"
# We want to have access to this file to end the observer


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


class MyHandler(FileSystemEventHandler):
    """Handler needed to manage file changes in our folder """
    @staticmethod
    def on_any_event(event):

        # if event.is_directory:
        #   event:  <FileMovedEvent: src_path='/home/carlos/Dropbox/Zoom/2019-11-27 14.41.58 Carlos David Loureda Parrado and carlos loureda parrado 941904988/zoom_0.mp4.tmp', dest_path='/home/carlos/Dropbox/Zoom/2019-11-27 14.41.58 Carlos David Loureda Parrado and carlos loureda parrado 941904988/zoom_0.mp4'>
        # event:  <FileMovedEvent: src_path='/home/carlos/Dropbox/Zoom/2019-11-27 14.41.58 Carlos David Loureda Parrado and carlos loureda parrado 941904988/audio_only.m4a.tmp', dest_path='/home/carlos/Dropbox/Zoom/2019-11-27 14.41.58 Carlos David Loureda Parrado and carlos loureda parrado 941904988/audio_only.m4a'>

        if True:
            if event.event_type == 'moved':
                if event.dest_path.endswith(".mp4"):
                    video_file = event.dest_path
                    folder_path = video_file[0: video_file.find("zoom_0.mp4")]
                    print("-> Video recorded at folder_path: ", folder_path)

                    # 1. upload folder to drive folder
                    # 2. get link to mp4 video
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


def main():
    if len(sys.argv) < 2:
        print(">> Please pass the url for the zoom meeting as parameter")
    else:
        zoom_url = sys.argv[1]
        open_zoom_meeting(zoom_url)
        # wait and listen for changes on Zoom folder ...
        listen_for_call_end()


# if __name__ == "__main__":
main()
