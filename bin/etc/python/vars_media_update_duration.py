#!/usr/bin/env python
from datetime import datetime
import iso8601
from microservices import VampireSquid
import argparse
import os
import json

__author__ = "Brian Schlining (modified by Rob Godfrey)"
__copyright__ = "Copyright 2022, Monterey Bay Aquarium Research Institute"

def main(filename: str, duration: str):
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    vamp_secret = os.environ["VAMPIRESQUID_CLIENT_SECRET"]
    vampire_squid = VampireSquid(vamp_url)
    media = vampire_squid.list_media_by_filename(filename)
    if len(media) == 1:
        print(f"Setting duration of {filename} to {duration}")
        duration = duration.split(':')
        duration_millis = int(duration[0]) * 3600000 + int(duration[1]) * 60000 + int(duration[2]) * 1000
        return vampire_squid.update_duration(media[0]['video_reference_uuid'],
                                                    duration_millis, 
                                                    client_secret=vamp_secret)
    elif len(media) > 1:
        print(
            f"Found {len(media)} media for {filename}. The filename is not unique in the database.")
        return dict()
    else:
        print(f"Media {filename} not found")
        return dict()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("media_file_name",
                        help="Just the file name of the media file")
    parser.add_argument(
            "new_duration", help="The duration of the video formatted \"HH:mm:ss\"")

    args = parser.parse_args()
    data = main(args.media_file_name, args.new_duration)
    print(json.dumps(data, indent=2))
