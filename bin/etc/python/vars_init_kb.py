#!/usr/bin/env python

import argparse
import zipfile
import requests

def main(kb_url, kb_data_file):
    json = _read_kb_as_json(kb_data_file)
    url = f"{kb_url}raw"
    print("Uploading KB to {}".format(kb_url))
    try:
        requests.post(url, data=json, headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException as e:
        # We expect a timeout. This is fine.
        pass

def _read_kb_as_json(kb_data_file):
    """ READ the zip file """
    kb_json = "{}"
    with zipfile.ZipFile(kb_data_file) as myzip:
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
        type=str)
    parser.add_argument("kb_data_file", help="The path to the KB JSON file. e.g. bin/etc/kb/mbari_kb.json.zip", 
        type=str)
    args = parser.parse_args()

    main(normalize_url(args.kb_url), args.kb_data_file)