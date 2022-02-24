#!/usr/bin/env python
import argparse
import iso8601
import os


from microservices import Annosaurus, VampireSquid

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2022, Monterey Bay Aquarium Research Institute"


#Latitude,Longitude,Depth,Temperature,Oxygen,Salinity,Date
#33.24405747,-164.7702751,95.075,15.6756,8.5349,34.5105,20170916T184219Z

def main(file_name, video_sequence_name: str, delimiter=","):
    anno_url = os.environ["ANNOSAURUS_URL"]
    anno_secret = os.environ["ANNOSAURUS_CLIENT_SECRET"]
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    annosaurus = Annosaurus(anno_url)
    vampire_squid = VampireSquid(vamp_url)
    media = vampire_squid.find_media_by_video_sequence_name(video_sequence_name)
    if media:
        data = __parse(file_name, delimiter)
        d = list(data)
        for m in media:
            print(f"Sending CTD/NAV data to be merged for {m['uri']}")
            annosaurus.merge(m["video_reference_uuid"], d, client_secret=anno_secret)
            pass

def __parse(file_name, delimiter):
    with open(file_name) as f:
        lines = f.readlines()

    for line in lines[1:]:
        parts = line.split(delimiter)
        latitude = float(parts[0])
        longitude = float(parts[1])
        depth = float(parts[2])
        temperature = float(parts[3])
        oxygen = float(parts[4])
        salinity = float(parts[5])
        date = iso8601.parse_date(parts[6]).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
        yield {"latitude": latitude, "longitude": longitude, "depth_meters": depth, "temperature_celsius": temperature, "oxygen_ml_l": oxygen, "salinity": salinity, "recorded_timestamp": date}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_sequence_name", help="Video Sequence Name is the deployment ID or expedition ID of the video. e.g. 'Doc Ricketts 1234'", 
        type=str)
    parser.add_argument("csv", help="The path to the CSV file containing the nav and ctd data", 
        type=str)
    args = parser.parse_args()
    main(args.csv, args.video_sequence_name)