from datetime import datetime
from microservices import VampireSquid
from pathlib import Path
import argparse
import io
import os
import requests
import urllib.request
import ffprobe

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
    p.remove()
    return checksum

def main(camera_id: str, deployment_id: str, uri: str, start_time: datetime):
    kb_url = os.environ["VAMPIRE_SQUID_URL"]
    kb_secret = os.environ["VAMPIRESQUID_CLIENT_SECRET"]
    vampire_squid = VampireSquid(kb_url)
    
    start_time_utc = start_time.astimezone(datetime.timezone.utc)
    time_str_full = start_time_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    time_str_compact = start_time_utc.strftime("%Y%m%dT%H%M%S.%fZ")

    print(f"Reading video metadata from {uri}")
    video_metadata = ffprobe.ffprobe(uri).video_metadata()
    mime_type = media_type(uri)
    print(f"Calculating checksum from {uri} (be patient)")
    checksum = sha512_from_uri(uri)

    xs = {
          "video_sequence_name" : deployment_id,
          "camera_id" : camera_id,
          "video_name" : f"{deployment_id} {time_str_compact}",
          "uri" : uri,
          "start_timestamp" : time_str_full,
          "duration_millis" : video_metadata.duration_millis,
          "container" : mime_type,
          "width" : video_metadata.width_pixels,
          "height" : video_metadata.height_pixels,
          "size_bytes" : video_metadata.size_bytes,
          "sha512" : f"{checksum}"
    }

    print(f"Registering {uri} in video asset manager")
    r = vampire_squid.create_media(xs["video_sequence_name"], 
      xs["video_name"], 
      xs["camera_id"], 
      xs["uri"], 
      xs["start_timestamp"], 
      client_secret=kb_secret)

    print("{uri} has been registered")
    [print(key,':',value) for key, value in r.items()]



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_id", help="Typically the ROV/AUV name", 
        type=str)
    parser.add_argument("deployment_id", help="The URL of the kb endpoints. e.g. http://localhost/kb/v1", 
        type=str)
    parser.add_argument("uri", help="The URL of the kb endpoints. e.g. http://localhost/kb/v1", 
        type=str)
    parser.add_argument("start_time", help="The URL of the kb endpoints. e.g. http://localhost/kb/v1", 
        type=str)
    parser.add_argument("camera_id", help="The URL of the kb endpoints. e.g. http://localhost/kb/v1", 
        type=str)
    args = parser.parse_args()
    main()