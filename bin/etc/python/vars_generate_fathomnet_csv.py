#!/user/bin/env python
from typing import Dict, List, Tuple
from microservices import VampireSquid, Annosaurus
import os
import json
import traceback

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2024, Monterey Bay Aquarium Research Institute"

def main(videoSequenceNames: List[str]) -> None:
    # print(f"Generating CSV for images from {videoSequenceNames}")
    # Get all video reference ids
    anno_url = os.environ["ANNOSAURUS_URL"]
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    vampire_squid = VampireSquid(vamp_url)

    # Get all media for the video sequence names
    media = []
    for videoSequenceName in videoSequenceNames:
        media += vampire_squid.find_media_by_video_sequence_name(videoSequenceName)

    # print(media)

    # Get all the bounding boxes for the video reference ids
    print("concept,url,x,y,width,height,timestamp,userdefinedkey,depth,pressure,latitude,longitude,observer,oxygen_ml_l,salinity,temperature")
    annosaurus = Annosaurus(anno_url)
    for m in media:
        annos = annosaurus.find_annotations(m['video_reference_uuid'])
        # print(annos)
        for a in annos:
            if 'image_references' in a and a['image_references'] and 'associations' in a:
                for association in a['associations']:
                    if association['link_name'] == 'bounding box':
                        try:
                            csv = __to_csv(m, a, association)
                            print(csv)
                        except Exception:
                            # print("Failed to parse: " + json.dumps(a))
                            # print(traceback.format_exc())
                            pass
                            
                        
        
                          
def __to_csv(media: List[Dict], annotation: List[Dict], association: List[Dict]) -> str:
    # concept, url, x, y, width, height, timestamp, userdefinedkey, depth, pressure, latitude, longitude, observer, oxygen_ml_l, salinity, temperature, 
    image_urls = [x['url'] for x in annotation['image_references'] if x['url'].endswith('png')]
    bounding_box = json.loads(association['link_value'])
    data = annotation.get('ancillary_data', {})
    
    return f"{annotation['concept']},{image_urls[0]},{bounding_box['x']},{bounding_box['y']},{bounding_box['width']},{bounding_box['height']},{annotation['recorded_timestamp']},{association['uuid']},{data.get('depth_meters', '')},{data.get('pressure_dbar', '')},{data.get('latitude', '')},{data.get('longitude', '')},{annotation['observer']},{data.get('oxygen_ml_l', '')},{data.get('salinity', '')},{data.get('temperature_celsius', '')}"





if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("videoSequenceNames", help="The video sequence names to upload to FathomNet", nargs='+')
    args = parser.parse_args()
    main(args.videoSequenceNames)