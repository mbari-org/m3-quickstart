#!/usr/bin/env python
import argparse
import iso8601
import math
import os
import pandas as pd

import json


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
        data = __parse_using_pandas(file_name, delimiter)
        d = list(data)
        # print(json.dumps(d, indent=4))
        for m in media:
            print(f"Sending CTD/NAV data to be merged for {m['uri']}")
            annosaurus.merge(m["video_reference_uuid"], d, client_secret=anno_secret)
            pass

def __parse_using_pandas(file_name, delimiter):
    data = pd.read_csv(file_name, delimiter=delimiter)
    for index, row in data.iterrows():
        altitude = __get_value("Alt", row, [999.9, 0])
        latitude = __get_value("Latitude", row)
        longitude = __get_value("Longitude", row)
        depth_meters = __get_value("Depth", row)
        temperature = __get_value("Temperature", row)
        # oxygen = __get_value("Oxygen", row)
        oxygen_mg_l = __get_value("oxygen_mg_per_l", row) # added to explicitly specify units
        oxygen_ml_l = __get_value("oxygen_ml_per_l", row)

        # if ml/L is not there, convert mg/L to ml/L
        if not oxygen_ml_l and oxygen_mg_l:
            oxygen_ml_l = round(oxygen_mg_l / 1.429, 5)
        
        salinity = __get_value("Salinity", row)

        date = iso8601.parse_date(row["Date"]).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        yield {"latitude": latitude, "longitude": longitude, 
          "depth_meters": depth_meters, "temperature_celsius": temperature, 
          "oxygen_ml_l": oxygen_ml_l, "salinity": salinity, 
          "recorded_timestamp": date, "altitude": altitude}


def __get_value(name, row, bad_values=None):
    v = None
    if name in row:
        v = row[name]
        if math.isnan(v):
            v = None
        if bad_values and v in bad_values:
            v = None
    return v

        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_sequence_name", help="Video Sequence Name is the deployment ID or expedition ID of the video. e.g. 'Doc Ricketts 1234'", 
        type=str)
    parser.add_argument("csv", help="The path to the CSV file containing the nav and ctd data", 
        type=str)
    args = parser.parse_args()
    main(args.csv, args.video_sequence_name)
