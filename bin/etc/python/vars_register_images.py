#!/usr/bin/env python
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from microservices import Annosaurus
from microservices import VampireSquid
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
import htmllistparse
import iso8601
import os
import re
import timeutil


@dataclass
class ImageData:
    url: str
    timestamp: datetime

def read_imagelist_from_web(url: str) -> List[ImageData]:
    cwd, listing = htmllistparse.fetch_listing(url, timeout=30)
    urls =  map(lambda x: f'{url}{x.name}', listing)
    return list(map(lambda x: ImageData(x, timeutil.datetime_from_name(x)), urls))


def __find_media(t: datetime, time_bounds: Dict[Dict, Tuple[datetime, datetime]]) -> Dict:
    for m, tb in time_bounds:
        if t >= tb[0] and t <= tb[1]:
            return m
    return None


def __find_annotation(t: datetime, annos: List[Dict]) -> Dict:
    for a in annos:
        if 'recorded_timestamp' in a:
            d = iso8601.parse_date(a['recorded_timestamp'])
            if d == t:
                return a
    return None


def __create_image(annotation: Dict,
                   media: Dict,
                   image_data: ImageData,
                   annosaurus: Annosaurus,
                   client_secret: str):
    hasAnno = False
    createImage = True
    if annotation:
        if annotation['image_references']:
            createImage = False
            hasAnno = True

    if not hasAnno:
        print(
            f"Creating annotation in {media['video_sequence_name']} at {image_data.timestamp.isoformat()}")
        annosaurus.create_annotation(media['video_reference_uuid'],
            'object', 'python-script', recorded_timestamp=image_data.timestamp,
            client_secret=client_secret)

    if createImage:
        print(
            f"Creating image in {media['video_sequence_name']} at {image_data.timestamp.isoformat()} using {image_data.url}")
        annosaurus.create_image(media['video_reference_uuid'],
                        image_data.url,
                        "imported image",
                        recorded_timestamp=image_data.timestamp,
                        client_secret=client_secret)



def __timebounds_for_images(image_data: ImageData) -> Tuple[datetime, datetime, int]:
    mint = None
    maxt = None
    for i in image_data:
        if mint is None or mint > i.timestamp:
            mint = i.timestamp
        if maxt is None or maxt < i.timestamp:
            maxt = i.timestamp
    dt = round((maxt - mint).total_seconds() * 1000)
    return mint, maxt, dt


def __find_or_create_image_media(video_sequence_name: str,
                                 image_data: ImageData,
                                 vampire_squid: VampireSquid,
                                 vamp_secret: str):
    media = vampire_squid.find_media_by_video_sequence_name(
        video_sequence_name)
    image_media = list(filter(lambda x: x['uri'].startswith("urn:imagecollection:org.mbari:"), media))
    if not image_media:
        print(f"Creating image collection media for {video_sequence_name}")
        video_name = f"{video_sequence_name} image collection"
        escaped_name = video_sequence_name.replace(" ", "_")
        uri = f"urn:imagecollection:org.mbari:{escaped_name}"
        time_bounds = __timebounds_for_images(image_data)
        print(time_bounds)
        return vampire_squid.create_media(video_sequence_name, 
              video_name, 
              media[0]['camera_id'], 
              uri, 
              time_bounds[0], 
              duration_millis=time_bounds[2], 
              client_secret=vamp_secret)
    else:
        print(f"Found image collection media for {video_sequence_name}")
        return image_media[0]


def main(video_sequence_name: str, url: str, force: bool = False):
    anno_url = os.environ["ANNOSAURUS_URL"]
    anno_secret = os.environ["ANNOSAURUS_CLIENT_SECRET"]
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    vamp_secret = os.environ["VAMPIRESQUID_CLIENT_SECRET"]

    vampire_squid = VampireSquid(vamp_url)
    media = vampire_squid.find_media_by_video_sequence_name(
        video_sequence_name)

    if media:
        image_data = read_imagelist_from_web(url)
        print(f"Found {len(image_data)} images")
        image_media = __find_or_create_image_media(video_sequence_name, image_data, vampire_squid, vamp_secret)
        if image_data:
            annosaurus = Annosaurus(anno_url)
            annos = annosaurus.find_annotations(image_media['video_reference_uuid'])
            for i in image_data:
                print(f"Registering image at {i.timestamp.isoformat()} using {i.url}")
                t = timeutil.datetime_from_name(i.url)
                a = __find_annotation(t, annos)
                __create_image(a, image_media, i, annosaurus, anno_secret)
    else:
        raise RuntimeError(
            f"Unable to find any media for video sequence name '{video_sequence_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_sequence_name", help="The deployment ID or expedition ID of the video. e.g. 'Doc Ricketts 1234'",
                        type=str)
    parser.add_argument("url", help="The URL to the video directory e.g. http://my.servername.org/media/D1234_EX1234",
                        type=str)
    args = parser.parse_args()
    main(args.video_sequence_name, args.url)
