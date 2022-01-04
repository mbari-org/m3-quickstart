from datetime import datetime
from pathlib import Path
from typing import NamedTuple
import argparse
import iso8601
import json
import subprocess
import sys

@dataclass
class VideoMetadata:
    name: str
    created: datetime
    duration_millis: int
    width_pixels: int
    height_pixels: int
    size_bytes: int

@dataclass
class FFProbeResult:
    name: str
    return_code: int
    json: str
    error: str

    def dict(self) -> dict:
        return json.loads(self.json)

    def video_metadata(self) -> VideoMetadata:
        json = self.dict()
        stream = json["streams"][0]
        file_format = json["format"]
        
        return VideoMetadata(self.name, 
            self.creation_time(),
            float(stream["duration"]) * 1000,
            int(stream["width"]),
            int(stream["height"]),  
            int(file_format["size"]))

    def creation_time(self):
        parts = self.name.split("_")
        try:
            return iso8601.parse_date(parts[1])
        except:
            file_format = json["format"]
            return iso8601.parse_date(file_format["tags"]["creation_time"])


def ffprobe(file_path) -> FFProbeResult:
    command_array = ["ffprobe",
                     "-v", "quiet",
                     "-print_format", "json",
                     "-show_format",
                     "-show_streams",
                     file_path]
    result = subprocess.run(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return FFProbeResult(name=file_path,
        return_code=result.returncode,
                         json=result.stdout,
                         error=result.stderr)