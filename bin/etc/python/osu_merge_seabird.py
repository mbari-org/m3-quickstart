#!/usr/bin/env python

import seabird
from seabird.cnv import fCNV
from typing import List
import datetime
import math
from microservices import Annosaurus, VampireSquid
import os

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2024, Monterey Bay Aquarium Research Institute"


def main(cnv_file: str, video_sequence_name: str, year: int) -> None:
    anno_url = os.environ["ANNOSAURUS_URL"]
    anno_secret = os.environ["ANNOSAURUS_CLIENT_SECRET"]
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    # Uncomment theses lines if you want to test the script without the microservices.
    # You'll need to comment out the lines below that use the microservices too.
    # data = __parse(cnv_file, year)
    # print(list(data))
    annosaurus = Annosaurus(anno_url)
    vampire_squid = VampireSquid(vamp_url)
    media = vampire_squid.find_media_by_video_sequence_name(video_sequence_name)
    if media:
        data = __parse(cnv_file, year)
        d = list(data)
        for m in media:
            print(f"Sending Seabird data to be merged for {m['uri']}")
            annosaurus.merge(m["video_reference_uuid"], d, client_secret=anno_secret)
            pass


def __parse(cnv_file: str, year: int):
    profile = fCNV(cnv_file)
    n = len(profile['timeJ'])
    for i in range(n):
    # for index, row in df.iterrows():
        timeJ = profile['timeJ'][i]
        altitude = profile["altM"][i]
     #    latitude = __get_value("Latitude", row)
     #    longitude = __get_value("Longitude", row)
        depth_meters = profile["DEPTH"][i]
        temperature = profile["potemperature"][i]
        oxygen = profile["oxygen_ml_L"][i]
     #    salinity = __get_value("Salinity", row)

        # https://info.seabird.com/2026_SeaBird_c-mult_c-June-Newsletter_landing-Page-2.html
        dt = datetime.datetime(year, 1, 1) + datetime.timedelta(days=(timeJ - 1))
        date = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        yield {
          #   "latitude": latitude,
          #   "longitude": longitude,
            "depth_meters": depth_meters,
            "temperature_celsius": temperature,
            "oxygen_ml_l": oxygen,
          #   "salinity": salinity,
            "recorded_timestamp": date,
            "altitude": altitude,
        }


def __get_value(name, row, bad_value=None):
    v = None
    if name in row:
        v = row[name]
        if math.isnan(v):
            v = None
        if bad_value and v == bad_value:
            v = None
    return v


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("cnv_file", help="The cnv file to convert to csv")
    parser.add_argument("video_sequence_name", help="Video Sequence Name is the deployment ID or expedition ID of the video. e.g. 'Doc Ricketts 1234'", 
        type=str)
    parser.add_argument("year", help="The year to use for the timeJ conversion", type=int)
    args = parser.parse_args()
    main(args.cnv_file, args.video_sequence_name, args.year)
