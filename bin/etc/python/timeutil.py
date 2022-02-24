from datetime import datetime

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2022, Monterey Bay Aquarium Research Institute"

__fmt = "%Y%m%dT%H%M%S.%fZ"

def compactIso(t: datetime) -> str:
    return t.strftime(__fmt)