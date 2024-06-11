#!/usr/bin/env python
import argparse
from typing import List
import htmllistparse
import vars_register_media

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2022, Monterey Bay Aquarium Research Institute"

def readDirListing(url: str) -> List[str]:
    cwd, listing = htmllistparse.fetch_listing(url, timeout=30)
    return map(lambda x: f'{url}{x.name}', listing)

def main(camera_id: str, deployment_id: str, url: str, extracttime: bool=False) -> None:
    urls = readDirListing(url)
    for uri in urls:
        print(f"Processing {uri}")
        try: 
            vars_register_media.main(camera_id, deployment_id, uri, extracttime)
        except Exception as e:
            print("An exception occured: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_id", help="Typically the ROV/AUV name", 
        type=str)
    parser.add_argument("deployment_id", help="The deployment ID or expedition ID of the video. e.g. 'Doc Ricketts 1234'", 
        type=str)
    parser.add_argument("url", help="The URL to the video directory e.g. http://my.servername.org/media/D1234_EX1234", 
        type=str)
    parser.add_argument('-e', '--extracttime', action='store_true', help="Extract the creation time from the video metadata. Default is to parse the filename" )
    args = parser.parse_args()
    main(args.camera_id, args.deployment_id, args.url, args.extracttime)