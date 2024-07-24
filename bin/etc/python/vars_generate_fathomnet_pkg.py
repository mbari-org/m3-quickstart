#!/user/bin/env python
from typing import Dict, List, Tuple
from microservices import VampireSquid, Annosaurus, Beholder
import os
import json
import traceback
import urllib
from pathlib import Path

__author__ = "Brian Schlining"
__copyright__ = "Copyright 2024, Monterey Bay Aquarium Research Institute"

def main(videoSequenceNames: List[str], outputDir: str) -> None:

    
    # Configure services
    anno_url = os.environ["ANNOSAURUS_URL"]
    vamp_url = os.environ["VAMPIRE_SQUID_URL"]
    beholder_url = os.environ["BEHOLDER_URL"]
    beholder_key = os.environ["BEHOLDER_API_KEY"]
    vampire_squid = VampireSquid(vamp_url)
    beholder = Beholder(beholder_url, beholder_key)
    annosaurus = Annosaurus(anno_url)

    # Create output directory
    outputPath = Path(outputDir)
    outputPath.mkdir(parents=True, exist_ok=True)

    # Open CSV file
    csv_filename = outputPath / "FathomNet.csv"
    csv_file = open(csv_filename, "w")
    csv_file.write("concept,url,x,y,width,height,timestamp,userdefinedkey,depth,pressure,latitude,longitude,observer,oxygen_ml_l,salinity,temperature\n")
 
    # Get all media for the video sequence names
    media = []
    for videoSequenceName in videoSequenceNames:
        media += vampire_squid.find_media_by_video_sequence_name(videoSequenceName)

    # Get all the bounding boxes for the video reference ids

    for m in media:
        process_media(m, outputPath, csv_file, annosaurus, beholder)
    csv_file.close()
    

                                               
def process_media(m: Dict, outputPath: Path, csv_file, annosaurus: Annosaurus, beholder: Beholder):
    annos = annosaurus.find_annotations(m['video_reference_uuid'])
    # print(annos)
    for a in annos:
        v = process_annotation(a, m, outputPath, beholder)
        if v:
            filename, csv = v
            csv_file.write(csv + "\n")
            print(f"Processed {filename}")
    return None

def process_annotation(a: Dict, m: Dict, outputPath: Path, beholder: Beholder):
    for association in a['associations']:
        if association['link_name'] == 'bounding box':

            # Grab image
            filename: str = None
            if 'image_references' in a and a['image_references']:
                # Download image
                image_urls = [x['url'] for x in a['image_references'] if x['url'].endswith('png')] 
                url = image_urls[0]
                filename = url.split("/")[-1]
                filepath = outputPath / filename
                if not filepath.exists():
                    print(f"Downloading {url} to {filepath}")
                    urllib.request.urlretrieve(url, filepath) 
            else:
                # Grab image with beholder
                media_url = m["uri"]
        
                if media_url.startswith("http"):
                    filename = m['video_sequence_name'] + "--" + a['imaged_moment_uuid'] + ".jpg"
                    filename = filename.replace(" ", "_")
                    p = outputPath / filename
                    if not p.exists():
                        print(f"Downloading {media_url} at {a['elapsed_time_millis']} to {p}")
                        beholder.capture_to_file(media_url, a['elapsed_time_millis'], str(p))


            # Return csv
            if filename:

                try:
                    csv = __to_csv(m, a, association, filename)
                    return (filename, csv)
                except Exception:
                    print("Failed to parse: " + json.dumps(a))
                    print(traceback.format_exc())
                    return None

    
                                                                                    
                          
def __to_csv(media: List[Dict], annotation: List[Dict], association: List[Dict], image_file: str) -> str:
    # concept, url, x, y, width, height, timestamp, userdefinedkey, depth, pressure, latitude, longitude, observer, oxygen_ml_l, salinity, temperature, 
    image_urls = [x['url'] for x in annotation['image_references'] if x['url'].endswith('png')]
    bounding_box = json.loads(association['link_value'])
    data = annotation.get('ancillary_data', {})
    
    return f"{annotation['concept']},{image_file},{bounding_box['x']},{bounding_box['y']},{bounding_box['width']},{bounding_box['height']},{annotation['recorded_timestamp']},{association['uuid']},{data.get('depth_meters', '')},{data.get('pressure_dbar', '')},{data.get('latitude', '')},{data.get('longitude', '')},{annotation['observer']},{data.get('oxygen_ml_l', '')},{data.get('salinity', '')},{data.get('temperature_celsius', '')}"




if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("outputDir", help="The output directory to write the data and images too.")
    parser.add_argument("videoSequenceNames", help="The video sequence names to upload to FathomNet", nargs='+')
    args = parser.parse_args()
    main(args.videoSequenceNames, args.outputDir)