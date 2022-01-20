from microservices import VampireSquid
from pathlib import Path
import argparse
import datetime
import io
import os
import requests
import subprocess
import urllib.request
import ffprobe

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2022, Monterey Bay Aquarium Research Institute"

def media_type(uri: str) -> str:
    r = requests.head(uri)
    return r.headers["Content-Type"]

def fetch(uri: str) -> Path:
    """Fetch a file from a URI"""
    return Path(urllib.request.urlretrieve(uri)[0])
    
def sha512(path: Path) -> str:
    """Calculate sha512"""
    p = subprocess.Popen(
        ['shasum', '-a', '512', path.as_posix()], stdout=subprocess.PIPE)
    j = ""
    for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
        j = j + line
    return j.split()[0]

def sha512_from_uri(uri: str) -> str:
    p = fetch(uri)
    checksum = sha512(p)
    p.unlink()  # Delete the file
    return checksum

def main(camera_id: str, deployment_id: str, uri: str):
    kb_url = os.environ["VAMPIRE_SQUID_URL"]
    kb_secret = os.environ["VAMPIRESQUID_CLIENT_SECRET"]
    vampire_squid = VampireSquid(kb_url)

    print(f"Reading video metadata from {uri}")
    video_metadata = ffprobe.ffprobe(uri).video_metadata()

    start_time_utc = video_metadata.creation_time.astimezone(datetime.timezone.utc)
    time_str_full = start_time_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    time_str_compact = start_time_utc.strftime("%Y%m%dT%H%M%S.%fZ")

    mime_type = media_type(uri)
    print(f"Calculating checksum from {uri} (be patient)")
    checksum = sha512_from_uri(uri)

    xs = {
          "camera_id" : camera_id,
          "container" : mime_type,
          "duration_millis" : video_metadata.duration_millis,
          "frame_rate" : video_metadata.frame_rate,
          "height" : video_metadata.height_pixels,
          "sha512" : f"{checksum}",
          "size_bytes" : video_metadata.size_bytes,
          "start_timestamp" : time_str_full,
          "uri" : uri,
          "video_codec": video_metadata.video_codec,
          "video_name" : f"{deployment_id} {time_str_compact}",
          "video_sequence_name" : deployment_id,
          "width" : video_metadata.width_pixels,
    }

    print(f"Registering {uri} in video asset manager")
    r = vampire_squid.create_media(xs["video_sequence_name"], 
      xs["video_name"], 
      xs["camera_id"], 
      xs["uri"], 
      xs["start_timestamp"], 
      client_secret=kb_secret, 
      duration_millis=xs["duration_millis"],
      width=xs["width"],
      height=xs["height"],
      size_bytes=xs["size_bytes"],
      sha512=xs["sha512"],
      frame_rate=xs["frame_rate"])

    print("{uri} has been registered")
    [print(key,':',value) for key, value in r.items()]



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_id", help="Typically the ROV/AUV name", 
        type=str)
    parser.add_argument("deployment_id", help="The deployment ID or expedition ID of the video. e.g. 'Doc Ricketts 1234'", 
        type=str)
    parser.add_argument("uri", help="The URL to the media file e.g. http://my.servername.org/media/D1234_20190201T120000Z.mp4", 
        type=str)
    args = parser.parse_args()
    main(args.camera_id, args.deployment_id, args.uri)