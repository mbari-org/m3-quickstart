#!/usr/bin/env python

import argparse
from .etc.python.microservices import VampireSquid

def main():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_id", help="The URL of the kb endpoints. e.g. http://localhost/kb/v1", 
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