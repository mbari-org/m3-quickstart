#!/usr/bin/env python
from datetime import datetime
import iso8601
from microservices import VampireSquid
import argparse
import os
import json

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2022, Monterey Bay Aquarium Research Institute"

def main(filename: str, start_timestamp: datetime):
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    vamp_secret = os.environ["VAMPIRESQUID_CLIENT_SECRET"]
    vampire_squid = VampireSquid(vamp_url)
    media = vampire_squid.list_media_by_filename(filename)
    if len(media) == 1:
        m = media[0]
        all_media = vampire_squid.find_media_by_video_name(m['video_name'])
        print(all_media)
        if len(all_media) == 1:
            print(f"Updating {filename} to start at {start_timestamp}")
            return vampire_squid.update_start_timestamp(m['video_reference_uuid'],
                                                        start_timestamp, 
                                                        client_secret=vamp_secret)
        else:
            video_name = generate_valid_name(m, start_timestamp, vampire_squid)
            print(
                f"Updating video name from {m['video_name']} to {video_name}")
            return vampire_squid.move_video_reference(m['video_reference_uuid'],
                                                      video_name,
                                                      start_timestamp,
                                                      client_secret=vamp_secret)
    elif len(media) > 1:
        print(
            f"Found {len(media)} media for {filename}. The filename is not unique in the database.")
        return dict()
    else:
        print(f"Media {filename} not found")
        return dict()


def generate_valid_name(media: dict, start_timestamp: datetime, vampire_squid: VampireSquid):
    n = 0
    new_video_name = media['video_name']
    while not is_valid_name(new_video_name, start_timestamp, media['duration_millis'], vampire_squid):
        if n > 0:
            new_video_name = f"{new_video_name} {n}"
        n += 1

    return new_video_name


def is_valid_name(video_name: str,  start_timestamp: datetime,  durationMillis: int,  vampire_squid: VampireSquid):
    all_media = vampire_squid.find_media_by_video_name(video_name)
    if len(all_media) == 0:
        return True
    else:
        for m in all_media:
            start1 = iso8601.parse_date(m['start_timestamp'])
            if start1 == start_timestamp and m['duration_millis'] == durationMillis:
                return True
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("media_file_name",
                        help="Just the file name of the media file")
    parser.add_argument(
        "start_timestamp", help="The start timestamp in ISO8601 format. yyyy-mm-ddThh:mm:ssZ")

    args = parser.parse_args()
    start_timestamp = iso8601.parse_date(args.start_timestamp)
    data = main(args.media_file_name, start_timestamp)
    print(json.dumps(data, indent=2))
