#!/usr/bin/env python3
import webbrowser
import sys

# ZOOM_MEETING_URL = "https://zoom.us/j/941904988?pwd=WitDeDZsbFljWlozdy9STVkyMEpYUT09"


def open_zoom_meeting(url):
    """Opens default browser with zoom link, as you would do clicking on the google calendar link"""
    webbrowser.open(url)


def main():
    if len(sys.argv) < 2:
        print(">> Please pass the url for the zoom meeting as parameter")
    else:
        zoom_url = sys.argv[1]
        open_zoom_meeting(zoom_url)


if __name__ == "__main__":
    main()
