from dataclasses import dataclass
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
    creation_time: datetime
    duration_millis: int
    width_pixels: int
    height_pixels: int
    size_bytes: int
    video_codec: str
    frame_rate: float

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
            int(file_format["size"]),
            stream["codec_name"],
            self.frame_rate())

    def creation_time(self):
        parts = self.name.split("_")
        try:
            return iso8601.parse_date(parts[1])
        except:
            file_format = self.dict()["format"]
            return iso8601.parse_date(file_format["tags"]["creation_time"])

    def frame_rate(self):
        json = self.dict()
        stream = json["streams"][0]
        return eval(stream["r_frame_rate"])


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