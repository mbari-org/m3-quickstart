from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from microservices import Annosaurus
from microservices import VampireSquid
from pathlib import Path
from typing import List
import argparse
import htmllistparse
import iso8601
import os
import re

@dataclass
class ImageData:
    timestamp: datetime
    url: str

def readDirListing(url: str) -> List[str]:
    cwd, listing = htmllistparse.fetch_listing(url, timeout=30)
    return map(lambda x: f'{url}/{x.name}', listing)

def readTimestamp(url: str) -> datetime:
    m = re.findall('\d{8}[T]\d{6,}', url)
    if m:
        d = m[-1]   
        if (len(d) > 15):
            d = d[:15] + '.' + d[15:]
        return iso8601.parse_date(d)
    m = re.findall('\d{14}', url)
    if m:
        d = m[-1][:8] + 'T' + m[-1][8:]
        return iso8601.parse_date(d)
    m = re.findall('\d{8}_\d{9}')
    if m:
        d = m[-1][:8] + "T" + m[-1][9:15] + "." + m[-1][15:]
        return iso8601.parse_date(d)
    raise RuntimeError(f'Failed to parse time from {url}')

        
def __processImage(annosaurus: Annosaurus, 
        annos: List,
        media,
        url: str,
        timestamp: datetime,
        client_secret: str):

    # Check that the timestamp is with in the media's times
    startTime = iso8601.parse_date(media['start_timestamp'])
    dt = timedelta(milliseconds=meda['duration_millis'])
    endTime = startTime + dt
    if timestamp < startTime or timestamp > endTime:
        raise RuntimeError(f"{timestamp.isoformat()} is not between {startTime.isoformat()} and {endTime.isoformat()}")
    
    hasAnno = False
    createImage = True
    for a in annos:
        if 'recorded_timestamp' in a:
            d = iso8601.parse_date(a['recorded_timestamp'])
            if d == timestamp:
                # Create image ONLY if one doesn't already exist
                if a['image_references']:
                    createImage = False
                hasAnno = True
                break

    if not hasAnno:
        annosaurus.create_annotation(media['video_reference_uuid'],
            'object', 'python-script', recorded_timestamp=timestamp,
            client_secret=client_secret)

    if createImage:
        annosaurus.create_image(media['video_reference_uuid'],
                        url, 
                        "imported image", 
                        recorded_timestamp=timestamp,
                        client_secret=client_secret)



def main(video_sequence_name: str, url: str):
    anno_url = os.environ["ANNOSAURUS_URL"]
    anno_secret = os.environ["ANNOSAURUS_CLIENT_SECRET"]
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]

    vampire_squid = VampireSquid(vamp_url)
    media = vampire_squid.find_media_by_video_sequence_name(video_sequence_name)
    if media:
        annosaurus = Annosaurus(anno_url)
        annos = annosaurus.find_annotations(media['video_reference_uuid'])
        urls = readDirListing(url)
        for imageUrl in urls:
            t = readTimestamp(imageUrl)
            __processImage(annosaurus, annos, media, imageUrl, t, client_secret=anno_secret)
    else:
        raise RuntimeError(f"Unable to find any media for video sequence name '{video_sequence_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("deployment_id", help="The deployment ID or expedition ID of the video. e.g. 'Doc Ricketts 1234'", 
        type=str)
    parser.add_argument("url", help="The URL to the video directory e.g. http://my.servername.org/media/D1234_EX1234", 
        type=str)
    args = parser.parse_args()
    main(args.deploymnet_id, args.url)