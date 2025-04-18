import argparse
from getpass import getpass
from microservices import Oni
import os

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2025, Monterey Bay Aquarium Research Institute"

def main(concept: str) -> None:
    oni_url = os.environ["ONI_URL"]
    oni = Oni(oni_url)
    # Prompt for username
    username = input('Enter your VARS username: ')

    # Prompt for password
    password = getpass()

    # Get beaerer token
    jwt = oni.login(username, password)

    # Delete the concept
    ok = oni.delete_concept(concept, jwt)
    if ok:
        print(f"Deleted concept: {concept}")
    else:
        print(f"Failed to delete concept: {concept}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("concept",
                        help="The concept name to delete",
                        type=str)
    args = parser.parse_args()
    main(args.concept)