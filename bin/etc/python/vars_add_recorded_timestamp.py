#!/usr/bin/env python

from datetime import timedelta
import os
import iso8601
from microservices import Annosaurus, VampireSquid


def main():
    anno_url = os.environ["ANNOSAURUS_URL"]
    anno_secret = os.environ["ANNOSAURUS_CLIENT_SECRET"]
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    vampire_squid = VampireSquid(vamp_url)
    annosaurus = Annosaurus(anno_url)
    ok_time = iso8601.parse_date("2000-01-01T00:00:00Z")
 
    # Get all video sequence names
    video_sequence_names = vampire_squid.list_video_sequence_names()
    print(f"Found {len(video_sequence_names)} video sequence names")

    # for each name, get it's media
    for name in video_sequence_names:
        all_media = vampire_squid.find_media_by_video_sequence_name(name)
        print(f"Found {len(all_media)} for deployment {name}")

        # for each media get it's annotations
        for media in all_media:
            # print(media)
            if 'start_timestamp' in media:
                uri = media['uri']
                if uri.startswith('file') or uri.startswith('http'):
                    start_time = iso8601.parse_date(media['start_timestamp'])
                    if start_time > ok_time:
                        print(f"{media['uri']} starts at {start_time.isoformat()}")
                        annos = annosaurus.find_annotations(media['video_reference_uuid'])


                        # if the annotation is missing a recorded date add it
                        for a in annos:
                            # if 'recorded_timestamp' not in a:
                            if 'elapsed_time_millis' in a:
                                dt = timedelta(milliseconds=a['elapsed_time_millis'])
                                recorded_timstamp = start_time + dt
                                # TODO update annotation
                                print(f"Setting annotation time to {recorded_timstamp.isoformat()}")
                                p = annosaurus.update_recorded_timestamp(a['imaged_moment_uuid'], recorded_timstamp, client_secret=anno_secret)
                                # print(p)


if __name__ == "__main__":
    main()