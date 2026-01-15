#!/usr/bin/env python
from microservices import VampireSquid
import argparse
import os
import json

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2026, Monterey Bay Aquarium Research Institute"

def main(filename: str, new_video_sequence_name: str, new_video_name: str, camera_id: str = None) -> dict:
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    vamp_secret = os.environ["VAMPIRESQUID_CLIENT_SECRET"]
    vampire_squid = VampireSquid(vamp_url)
    media = vampire_squid.list_media_by_filename(filename)
    if len(media) == 1:
        print(f"Updating names of {filename} to sequence: {new_video_sequence_name}, video: {new_video_name}")
        data = dict()
        if (camera_id is not None):
            data['camera_id'] = camera_id
        else:
            data['camera_id'] = media[0]['camera_id']
        data["video_reference_uuid"] = media[0]['video_reference_uuid']
        data['video_sequence_name'] = new_video_sequence_name
        data['video_name'] = new_video_name
        data['start_timestamp'] = media[0]['start_timestamp']
        data['duration_millis'] = media[0]['duration_millis']
        return vampire_squid.update_media(data, client_secret=vamp_secret)
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

    parser.add_argument("new_video_sequence_name",
                        help="The new video sequence name to set")
    parser.add_argument("new_video_name",
                        help="The new video name to set")
    parser.add_argument("--camera_id",
                        help="Option camera ID if you want to set it explicitly")

    args = parser.parse_args()
    data = main(args.media_file_name, args.new_video_sequence_name, args.new_video_name, args.camera_id)
    print(json.dumps(data, indent=2))