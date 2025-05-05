#!/usr/bin/env python

import iso8601
from microservices import Annosaurus
import argparse
import os
import json

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2025, Monterey Bay Aquarium Research Institute"


def main(filename: str, anno_url: str, client_secret: str) -> None:
    # Read json file
    data = []
    with open(filename, 'r') as f:
        data = json.load(f)
    annosaurus = Annosaurus(anno_url)
    created = annosaurus.create_annotations(data, client_secret)
    if created:
        print(f"Created {len(data)} annotations")
    else:
        print("Failed to create annotations")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",
                        help="The json file to read",
                        type=str)
    args = parser.parse_args()
    anno_url = os.environ["ANNOSAURUS_URL"]
    client_secret = os.environ["ANNOSAURUS_CLIENT_SECRET"]
    if not anno_url:
        raise ValueError("ANNOSAURUS_URL environment variable is not set")
    if not client_secret:
        raise ValueError("ANNOSAURUS_CLIENT_SECRET environment variable is not set")
    if not os.path.exists(args.filename):
        raise ValueError(f"File {args.filename} does not exist")
    if not os.path.isfile(args.filename):
        raise ValueError(f"File {args.filename} is not a file")
    if not args.filename.endswith(".json"):
        raise ValueError(f"File {args.filename} is not a json file")
    if not os.access(args.filename, os.R_OK):
        raise ValueError(f"File {args.filename} is not readable")
    main(args.filename, anno_url, client_secret)
    
    




