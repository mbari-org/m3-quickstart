from datetime import datetime
import iso8601
from microservices import VampireSquid
import argparse
import os
import json

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2022, Monterey Bay Aquarium Research Institute"

def main(video_sequence_name: str) -> None:
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    vamp_secret = os.environ["VAMPIRESQUID_CLIENT_SECRET"]
    vampire_squid = VampireSquid(vamp_url)
    video_sequence = vampire_squid.find_video_sequence_by_name(video_sequence_name)
    if 'uuid' in video_sequence:
        print(f"Deleting video sequence {video_sequence_name}")
        vampire_squid.delete_video_sequence(video_sequence['uuid'], client_secret=vamp_secret)
    else:
        print(f"Video sequence {video_sequence_name} not found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_sequence_name",
                        help="The name of the video sequence (aka deployment id) to delete",
                        type=str)
    args = parser.parse_args()
    main(args.video_sequence_name)