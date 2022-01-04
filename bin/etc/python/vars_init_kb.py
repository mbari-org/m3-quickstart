#!/usr/bin/env python

import argparse
import zipfile
import requests

def main(kb_url):
    json = _read_kb_as_json()
    url = f"{kb_url}raw"
    print("Uploading KB to {}".format(kb_url))
    try:
        requests.post(url, data=json, headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException as e:
        # We expect a timeout. This is fine.
        pass

def _read_kb_as_json():
    """ READ the zip file """
    kb_json = "{}"
    with zipfile.ZipFile("etc/kb/mbari_kb.json.zip") as myzip:
        with myzip.open("mbari_kb.json") as myfile:
            kb_json = myfile.read()
    return kb_json

def normalize_url(kb_url):
    """ Normalize the URL """
    if not kb_url.endswith('/'):
        kb_url += '/'
    return kb_url

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kb_url", help="The URL of the kb endpoints. e.g. http://localhost/kb/v1", 
        type=int)
    args = parser.parse_args()

    main(normalize_url(args.kb_url))