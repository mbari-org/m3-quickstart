from datetime import datetime, time, timedelta
from typing import List, Dict
from urllib.parse import quote
import iso8601
import json
import requests
import subprocess
import sys
import time as pytime
import timeutil


__author__ = "Brian Schlining"
__copyright__ = "Copyright 2018, Monterey Bay Aquarium Research Institute"

JsonArray = List[Dict]


def datetime_to_iso8601(t: str) -> datetime:
    dt = iso8601.parse_date(t)
    return dt


class AuthenticationError(Exception):
    """Exception raised for errors during authentication.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class JWTAuthtication(object):

    def __init__(self, base_url: str):
        if base_url.endswith("/"):
            base_url = base_url[0:-1]
        self.base_url = base_url

    def authorize(self, client_secret: str, jwt: str) -> str:
        """Fetch a JWT authentication token if needed """
        if jwt:
            pass
        elif client_secret:
            jwt = self.authenticate(client_secret)
        else:
            raise AuthenticationError("No jwt or client_secret were provided")

        if not jwt:
            raise AuthenticationError(
                "Failed to authenticate with your client_secret")
        return jwt

    def authenticate(self, client_secret: str) -> str:
        """Call the authentication endpoint to retrieve a JWT todken as a string"""
        url = "{}/auth".format(self.base_url)
        headers = {"Authorization": "APIKEY {}".format(client_secret)}

        r = requests.post(url, headers=headers)
        try:
            auth_response = r.json()
            return auth_response["access_token"]
        except json.decoder.JSONDecodeError:
            print("-- BAD Authentication: {} returned: \n{}".format(url, r.text))
            return None

    def _auth_header(self, jwt: str) -> Dict:
        """Format """
        return {"Authorization": "Bearer " + jwt}


class VampireSquid(JWTAuthtication):
    """ Encapsulate REST calls to the video-asset manager

    Some terms:

       A `video sequence` is essentially a camera/rov/auv deployment

       A `video` is a segment of video in video seqeunce. Often a video
       may have several representations: e.g. master, mezzanine and proxy
       versions. A video will contain one or more video references.

       A `video reference` is information about a single video file. Usually,
       it has a URI that is a URL to a video file on a web server.

       A `media` is a simple, yet complete, metadata view of a video reference. Media
       are often the easiest unit to work with.

    Typical usage:
    1. Find the name of the video sequence of interest. (list_video_sequence_names)
    2. Look up the video sequence by name (find_video_sequence_by_name)
        - This returns all media that compose a single video sequence.
        - This might be all you need.
        - If you want a simpiler view, grab the video_reference.uuid and use
        `find_media_by_uuid` to get a media view of a video reference.

    """

    def __init__(self, base_url: str):
        JWTAuthtication.__init__(self, base_url)

    def list_video_sequence_names(self) -> List[str]:
        """List all available video sequence names"""
        url = "{}/videosequences/names".format(self.base_url)
        return requests.get(url).json()

    def list_media_by_filename(self, filename: str) -> JsonArray:
        """Find all media with a given filename"""
        url = "{}/media/videoreference/filename/{}".format(self.base_url, quote(filename, safe=''))
        return requests.get(url).json()

    def find_media_by_sha512(self, sha512: str) -> Dict:
        """Find a single media by its sha512 checksum"""
        url = "{}/media/sha512/{}".format(self.base_url, sha512)
        return requests.get(url).json()

    def find_media_by_uri(self, uri: str) -> Dict:
        """Find a single media by it's uri"""
        url = "{}/media/uri/{}".format(self.base_url, quote(uri, safe=''))
        r = requests.get(url)
        # r.raise_for_status()
        # print(r)
        # print(r.text)
        if r.status_code == 200:
            return r.json()
        else:
            return dict()

    def find_media_by_video_name(self, video_name: str) -> JsonArray:
        """Find all media belonging to a video"""
        url = "{}/media/video/{}".format(self.base_url, video_name)
        r = requests.get(url)
        return r.json()

    def find_media_by_video_sequence_name(self, video_sequence_name: str) -> JsonArray:
        """Find all media belonging to a video sequence"""
        url = "{}/media/videosequence/{}".format(
            self.base_url, video_sequence_name)
        r = requests.get(url)
        # r.raise_for_status()
        # print(r)
        # print(r.text)
        return r.json()

    def find_media_by_video_reference_uuid(self, video_reference_uuid: str) -> Dict:
        """Find a single media by its video_reference_uuid"""
        url = "{}/media/videoreference/{}".format(
            self.base_url, video_reference_uuid)
        r = requests.get(url)
        # print(r)
        # print(r.text)
        return r.json()

    def delete_media_by_video_reference_uuid(self,
                                             video_reference_uuid: str,
                                             client_secret: str = None,
                                             jwt: str = None) -> None:
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        url = "{}/videoreferences/{}".format(self.base_url,
                                             video_reference_uuid)
        requests.delete(url, headers=headers)

    def find_concurrent_media(self, video_reference_uuid: str) -> JsonArray:
        """Find all media in the same video sequence that overlap in time
        with the one whos primary key you provide"""
        url = "{}/media/concurrent/{}".format(
            self.base_url, video_reference_uuid)
        return requests.get(url).json()

    def find_media_by_media(self, media: Dict) -> Dict:
        """Find a media base on an example media. A match is based
           on equality. uri for media that use a "urn". sha512 for urls.
           The video_reference_uuid is used if other lookups do not
           return a match
           """
        other: Dict = None
        if "uri" in media:
            uri = media["uri"]
            if uri.startswith("urn"):
                other = self.find_media_by_uri(uri)
            else:
                if "sha512" in media:
                    other = self.find_media_by_sha512(media['sha512'])

        if not other and "video_reference_uuid" in media:
            other = self.find_media_by_video_reference_uuid(
                media["video_reference_uuid"])

        return other

    def create_media(self,
                     video_sequence_name: str,
                     video_name: str,
                     camera_id: str,
                     uri: str,
                     start_timestamp,  # could be a datetime or a string
                     video_reference_uuid: str = None,
                     client_secret: str = None,
                     jwt: str = None,
                     **kwargs) -> Dict:
        """
        Create a media. Required arguments are enumerated. Optional parameters that
        can be included are: duration_millis: int, container: str, video_codec: str,
        audio_codec: str, width: int, height: int, frame_rate: float, size_bytes: int,
        video_description: str, sha512: str = None. Note that when working with videos
        with 'http' uris the sha512 argument is HIGHTLY recommended.

        start_timestamp should be either an iso8601 string or a datetime obj

        Returns None if the start_timestamp is invalid
        """
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        data = {"video_sequence_name": video_sequence_name,
                "video_name": video_name,
                "camera_id": camera_id,
                "uri": uri}

        if video_reference_uuid:
            data["video_reference_uuid"] = video_reference_uuid

        # Add start_timestamp as iso8601 string
        if isinstance(start_timestamp, datetime):
            data["start_timestamp"] = start_timestamp.isoformat()
        else:
            try:
                # Parse str to make sure it's iso8601
                t = iso8601.parse_date(start_timestamp)
                data["start_timestamp"] = start_timestamp
            except:
                print("{} is not a valid is08601 timestamp".format(start_timestamp))

        if "start_timestamp" in data:
            for key, value in kwargs.items():
                data[key] = value
            url = "{}/media".format(self.base_url)
            r = requests.post(url, data=data, headers=headers)
            return r.json()
        else:
            return None

    def find_video_sequence_by_name(self, name: str) -> Dict:
        ""
        url = "{}/videosequences/name/{}".format(self.base_url, name)
        r = requests.get(url)
        r.raise_for_status()
        # print(r)
        # print(r.text)
        return requests.get(url).json()

    def delete_video_sequence(self,
                              video_sequence_uuid: str,
                              client_secret: str = None,
                              jwt: str = None) -> None:
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        url = "{}/videosequences/{}".format(self.base_url, video_sequence_uuid)
        requests.delete(url, headers=headers)

    def update_checksum(self,
                         video_reference_uuid: str,
                         sha512: str,
                         client_secret: str = None,
                         jwt: str = None):
        jwt = self.authorize(client_secret, jwt)
        url = "{}/videoreferences/{}".format(self.base_url,
                                             video_reference_uuid)
        data = dict()
        data['sha512'] = sha512
        headers = self._auth_header(jwt)
        return requests.put(url, data=data, headers=headers).json()

    def move_video_reference(self,
                             video_reference_uuid: str,
                             video_name: str,
                             start_timestamp: datetime,
                             client_secret: str = None,
                              jwt: str = None):
        """Move a video reference to a new video and start_timestamp

        Args:
            video_reference_uuid (str): The UUID of an existing video reference
            video_name (str): The new name of a video reference
            start_timestamp (str): The new start_timestamp of a video reference
            client_secret (str, optional): authorization secret. Defaults to None.
            jwt (str, optional): JWT authorization. Defaults to None.

        Returns:
            Dict: Media object as dict. None if the video_reference_uuid is not found or 
                  if it can't be changed using the give parameters
        """
        jwt = self.authorize(client_secret, jwt)
        media = self.find_media_by_video_reference_uuid(video_reference_uuid)
        if media:
            url = "{}/media/move/{}".format(self.base_url,
                                                video_reference_uuid)
            data = dict()
            data['start_timestamp'] = start_timestamp.isoformat()
            data['duration_millis'] = media['duration_millis']
            data['video_name'] = video_name
            headers = self._auth_header(jwt)
            return requests.put(url, data=data, headers=headers).json()
        else: 
            return None



    def update_start_timestamp(self,
                               video_reference_uuid: str,
                               start_timestamp: datetime,
                               client_secret: str = None,
                               jwt: str = None):
        """Update the Start Timestamp of a Media

        Args:
            video_reference_uuid (str): The UUID of the media
            start_timestamp (datetime): The new timestamp it MUST have a timezone set. 
                e.g. d = datetime.datetime.now(datetime.timezone.utc)
            client_secret (str, optional): The client secret used for authentication. Defaults to None. Not 
                required if jwt is provided
            jwt (str, optional): The authentication token. Defaults to None.

        Returns:
            Media: The updated media object as JSON/dict
        """
        jwt = self.authorize(client_secret, jwt)
        url = "{}/media/{}".format(self.base_url,
                                             video_reference_uuid)
        data = dict()
        data['start_timestamp'] = start_timestamp.isoformat()
        headers = self._auth_header(jwt)
        return requests.put(url, data=data, headers=headers).json()



    def update_duration(self,
                               video_reference_uuid: str,
                               duration_millis: int,
                               client_secret: str = None,
                               jwt: str = None):
        """Update the duration of a media record (added by Rob)

        Args:
            video_reference_uuid (str): The UUID of the media
            duration_millis): The new duration of the media in milliseconds 
            client_secret (str, optional): The client secret used for authentication. Defaults to None. Not 
                required if jwt is provided
            jwt (str, optional): The authentication token. Defaults to None.

        Returns:
            Media: The updated media object as JSON/dict
        """
        jwt = self.authorize(client_secret, jwt)
        url = "{}/media/{}".format(self.base_url,
                                             video_reference_uuid)
        data = dict()
        data['duration_millis'] = duration_millis
        headers = self._auth_header(jwt)
        return requests.put(url, data=data, headers=headers).json()



    def update_media(self, 
                     media: JsonArray,
                     client_secret: str = None,
                     jwt: str = None) -> JsonArray:
        jwt = self.authorize(client_secret, jwt)
        url = "{}/media/{}".format(self.base_url, media['video_reference_uuid'])
        headers = self._auth_header(jwt)
        return requests.put(url, data=media, headers=headers).json()


class Annosaurus(JWTAuthtication):
    """Encapsulate REST calls to the annotation service

    """

    def __init__(self, base_url: str):
        JWTAuthtication.__init__(self, base_url)

    def count_group_by_video_reference_uuid(self) -> JsonArray:
        url = "{}/observations/counts".format(self.base_url)
        return requests.get(url).json()

    def count_by_video_reference_uuid(self, video_reference_uuid: str):
        url = "{}/observations/videoreference/count/{}".format(
            self.base_url, video_reference_uuid)
        return requests.get(url).json()

    def find_annotations(self, video_reference_uuid: str,
                         timeout: int = 20) -> JsonArray:
        """Find all annotations for a specific media/video"""
        # url = "{}/annotations/videoreference/chunked/{}?timeout={}".format(
        #     self.base_url, video_reference_uuid, timeout)
        url = "{}/fast/videoreference/{}".format(
            self.base_url, video_reference_uuid)
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def find_imaged_moments(self, video_reference_uuid: str,
                            pagesize: int = 20,
                            timeout: int = 20) -> JsonArray:
        """Find all imaged_moments for a specific media/video"""
        url = "{}/imagedmoments/videoreference/chunked/{}?pagesize={}timeout={}".format(
            self.base_url, video_reference_uuid, pagesize, timeout)
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def find_images(self, video_reference_uuid) -> JsonArray:
        url = "{}/images/videoreference/{}".format(
            self.base_url, video_reference_uuid)
        return requests.get(url).json()

    def find_imaged_moment_by_image(self, image_reference_uuid: str) -> Dict:
        url = "{}/imagedmoments/imagereference/{}".format(
            self.base_url, image_reference_uuid)
        print(url)
        s = requests.get(url).json()
        # print(s)
        return s
        # return requests.get(url).json()

    def find_video_reference_info(self, video_reference_uuid: str) -> Dict:
        url = "{}/videoreferences/videoreference/{}".format(
            self.base_url, video_reference_uuid)
        try:
            r = requests.get(url)
            r.raise_for_status()
            # print(r)
            # print(r.text)
            return r.json()
        except:
            return None

    def delete_video_reference_info(self,
                                    uuid: str,
                                    client_secret: str = None,
                                    jwt: str = None) -> None:
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        url = "{}/videoreferences/{}".format(self.base_url, uuid)
        requests.delete(url, headers=headers)

    def create_annotations(self,
                           annotations: JsonArray,
                           client_secret: str = None,
                           jwt: str = None) -> JsonArray:
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        headers["Content-Type"] = "application/json"
        url = "{}/annotations/bulk".format(self.base_url)
        # j = json.dumps(annotations)
        # print(j)

        r = requests.post(url, headers=headers, json=annotations)
        # print(r)
        # print(r.text)
        return r.json()

    def create_annotation(self,
                          video_reference_uuid: str,
                          concept: str,
                          observer: str,
                          elapsed_time_millis: int = None,
                          recorded_timestamp: datetime = None,
                          timecode: str = None,
                          client_secret: str = None,
                          jwt: str = None) -> Dict:

        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        data = {"video_reference_uuid": video_reference_uuid,
                "concept": concept,
                "observer": observer}
        if elapsed_time_millis:
            data['elapsed_time_millis'] = elapsed_time_millis
        elif recorded_timestamp:
            data['recorded_timestamp'] = "{}".format(
                recorded_timestamp.isoformat())
        elif timecode:
            data['timecode'] = timecode

        url = "{}/annotations".format(self.base_url)
        r = requests.post(url, data=data, headers=headers)
        # print(r)
        # print(r.text)
        # print(data)
        return r.json()

        # return requests.post(url, data=data, headers=headers).json()

    def create_image(self,
                     video_reference_uuid: str,
                     url: str,
                     description: str = None,
                     elapsed_time_millis: int = None,
                     recorded_timestamp: datetime = None,
                     timecode: str = None,
                     client_secret: str = None,
                     jwt: str = None):

        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)

        data = {"video_reference_uuid": video_reference_uuid,
                "url": url}

        if description:
            data['description'] = description

        if elapsed_time_millis:
            data['elapsed_time_millis'] = elapsed_time_millis
        elif recorded_timestamp:
            data['recorded_timestamp'] = "{}".format(
                recorded_timestamp.isoformat())
        elif timecode:
            data['timecode'] = timecode

        url = "{}/images".format(self.base_url)
        r = requests.post(url, data=data, headers=headers)
        # print(r)
        # print(r.text)
        # print(data)
        return r.json()

    def create_association(self,
                           observation_uuid: str,
                           association: Dict,
                           client_secret: str = None,
                           jwt: str = None) -> Dict:

        if 'link_name' not in association:
            raise ValueError(
                "association dict needs at least a 'link_name' key")

        jwt = self.authorize(client_secret, jwt)
        url = "{}/associations".format(self.base_url)
        association['observation_uuid'] = observation_uuid
        headers = self._auth_header(jwt)
        return requests.post(url, data=association, headers=headers).json()

    def delete_annotations_for_video(self,
                                     video_reference_uuid: str,
                                     client_secret: str = None,
                                     jwt: str = None):
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        url = "{}/fast/videoreference/{}".format(
            self.base_url, video_reference_uuid)
        return requests.delete(url, headers=headers)

    def delete_annotation(self,
                          observation_uuid: str,
                          client_secret: str = None,
                          jwt: str = None):
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        url = "{}/observations/{}".format(self.base_url, observation_uuid)
        return requests.delete(url, headers=headers)

    def delete_imaged_moment(self, imaged_moment_uuid: str,
                             client_secret: str = None,
                             jwt: str = None):
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        url = "{}/imagedmoments/{}".format(self.base_url, imaged_moment_uuid)
        return requests.delete(url, headers=headers)

    def merge(self, video_reference_uuid: str,
              rows: List[Dict],
              client_secret: str = None,
              jwt: str = None):
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        headers['Content-type'] = "application/json"
        url = "{}/ancillarydata/merge/{}".format(self.base_url, video_reference_uuid)
        body = json.dumps(rows)
        return requests.put(url, headers=headers, data=body).json()

    def update_recorded_timestamp(self, imaged_moment_uuid: str,
               recorded_timestamp: datetime,
               client_secret: str = None,
               jwt: str = None):
        jwt = self.authorize(client_secret, jwt)
        headers = self._auth_header(jwt)
        headers['Content-type'] = "application/json"
        url = f"{self.base_url}/index/tapetime"
        d = [{"uuid": imaged_moment_uuid, "recorded_timestamp": recorded_timestamp.isoformat()}]   
        body = json.dumps(d)
        return requests.put(url, headers=headers, data=body).json()

class M3(object):

    def __init__(self, annosaurus: Annosaurus, vampire_squid: VampireSquid):
        self.annosaurus = annosaurus
        self.vampire_squid = vampire_squid

    def find_annotations(self, video_sequence_name: str) -> JsonArray:
        media = self.vampire_squid.find_media_by_video_sequence_name(video_sequence_name)
        # print(f"Found {len(media)} media")
        annos = []
        for m in media:
            xs = self.annosaurus.find_annotations(m['video_reference_uuid'])
            annos.extend(xs)
        return annos

    def find_concurrent_annotations(self, video_reference_uuid: str) -> JsonArray:
        """Find annotations from other media in the same video sequence that occur
        within the time bounds of your chosen media. Re-indexes the annotations
        using the elapsed time of the selected media"""

        # --- 1. Get the time bounds of your video
        media = self.vampire_squid.find_media_by_video_reference_uuid(
            video_reference_uuid)
        start = iso8601.parse_date(media['start_timestamp'])
        end = start + timedelta(milliseconds=media['duration_millis'])

        concurrent_media = self.vampire_squid.find_concurrent_media(
            video_reference_uuid)

        annotations = self.annosaurus.find_annotations(video_reference_uuid)
        for c in concurrent_media:
            new_annos = self.annosaurus.find_annotations(
                c['video_reference_uuid'])
            for a in new_annos:
                if 'recorded_timestamp' in a:
                    t = iso8601.parse_date(a['recorded_timestamp'])
                    if t >= start and t <= end:

                        # Calculate elapsed time relative to our chosen media
                        dt = t - start
                        millis = dt.total_seconds() * 1000
                        a['elapsed_time_millis'] = int(millis)

                        # print("ET={}\tT={}".format(
                        #     a['elapsed_time_millis'], a['recorded_timestamp']))

                        annotations.append(a)

        return annotations

    def find_concurrent_images(self, video_reference_uuid: str) -> JsonArray:
        """Find iamges from other media in the same video sequence that occur
        within the time bounds of your chosen media"""

        # --- 1. Get the time bounds of your video
        media = self.vampire_squid.find_media_by_video_reference_uuid(
            video_reference_uuid)
        start = iso8601.parse_date(media['start_timestamp'])
        end = start + timedelta(milliseconds=media['duration_millis'])

        # --- 2. Find other media that overlap our media
        concurrent_media = self.vampire_squid.find_concurrent_media(
            video_reference_uuid)

        # Fetch all the images
        images = self.annosaurus.find_images(video_reference_uuid)
        for c in concurrent_media:
            new_images = self.annosaurus.find_images(
                c['video_reference_uuid'])
            for i in new_images:
                if 'recorded_timestamp' in i:
                    t = iso8601.parse_date(i['recorded_timestamp'])
                    if t >= start and t <= end:

                        # Calculate elapsed time relative to our chosen media
                        dt = t - start
                        millis = dt.total_seconds() * 1000
                        i['elapsed_time_millis'] = int(millis)

                        images.append(i)

        return images

    def delete_by_video_uri(self, uri: str,
                            client_secret: str = None,
                            jwt: str = None) -> str:
        media = self.vampire_squid.find_media_by_uri(uri)
        if media is None:
            print("No media was found with URI of `uri`")
            return None
        else:
            uuid = media['video_reference_uuid']
            r = self.annosaurus.delete_annotations_for_video(
                uuid, client_secret=client_secret, jwt=jwt)
            print(r.status_code)
            return r.text

    def delete_empty_video_sequence(self,
                                    video_sequence_name: str,
                                    anno_client_secret: str = None,
                                    anno_jwt: str = None,
                                    vamp_client_secret: str = None,
                                    vamp_jwt: str = None) -> None:

        print("-- Examining VideoSequence '{}' for deleting".format(video_sequence_name))

        # Fetch all media for a video sequence
        media = self.vampire_squid.find_media_by_video_sequence_name(
            video_sequence_name)

        # Iterate over each media
        for m in media:

            video_reference_uuid = m['video_reference_uuid']

            # Check annotations ... if any exist report it
            n = self.annosaurus.count_by_video_reference_uuid(
                video_reference_uuid)

            if n['count'] != 0:
                print(
                    "\tWARNING: VideoReference '{}' has {} annotations. Unable to delete".format(m['uri'], n['count']))
            else:
                # If none exist, lookup cached video reference
                vr = self.annosaurus.find_video_reference_info(
                    video_reference_uuid)

                # If it exists delete it, then delete media
                if vr:
                    print("\tDeleting VideoReferenceInfo for '{}' [UUID: {}]".format(
                        vr['mission_id'], vr['uuid']))
                    self.annosaurus.delete_video_reference_info(
                        vr['uuid'], client_secret=anno_client_secret)

                # Delete media
                print("\tDeleting VideoReference '{}' [UUID: {}]".format(
                    m['uri'], m['video_reference_uuid']))
                self.vampire_squid.delete_media_by_video_reference_uuid(
                    video_reference_uuid, client_secret=vamp_client_secret)

        # Fetch all media again. If non exists, fetch video sequence
        media = self.vampire_squid.find_media_by_video_sequence_name(
            video_sequence_name)

        if len(media) == 0:
            video_sequence = self.vampire_squid.find_video_sequence_by_name(
                video_sequence_name)
            if video_sequence:
                print("\tDeleting VideoSequence named '{}' [UUID: {}]".format(
                    video_sequence_name, video_sequence['uuid']))
                self.vampire_squid.delete_video_sequence(
                    video_sequence['uuid'], client_secret=vamp_client_secret)
        else:
            print("\tWARNING: VideoSequence '{}' is not empty. Unable to delete".format(
                video_sequence_name))

    def map_to_media(self, annotations: List[Dict], uri: str) -> List[Dict]:
        """Looks up a media by it's URI and associates all the annotations in a colleciton
        wit that media. If no media is found, then an empty list is returned"""
        media = vampire_squid.find_media_by_uri(uri)
        if media:
            for a in annotations:
                a['video_reference_uuid'] = media['video_reference_uuid']
            return annotations
        else:
            print("{} not found at {}".format(uri, vampire_squid.base_url))
            return []

    def move_annotations(self, uri: str, annotations: JsonArray) -> JsonArray:
        media = self.vampire_squid.find_media_by_uri(uri)
        updated_annotations = []
        if media:
            for a in annotations:
                a['video_reference_uuid'] = media['video_reference_uuid']
            updated_annotations = annotations
        return updated_annotations

    @staticmethod
    def remove_duplicate_elapsed_times(annotations) -> JsonArray:
        """There's often more than one observation in the same frame. Skip duplicate times"""
        # TODO need to get fancier. Key should be video_uuid + elapsed_time
        checked_elapsed_times = set()
        checked_annotations = list()
        for a in annotations:
            t = a['elapsed_time_millis']
            if t not in checked_elapsed_times:
                checked_elapsed_times.add(t)
                checked_annotations.append(a)
        return checked_annotations


class VarsKnowledgebase(object):

    def __init__(self, base_url: str):
        self.base_url = base_url

    def find_descendants(self, concept: str) -> Dict:
        url = "{}/phylogeny/down/{}".format(self.base_url, concept)
        return requests.get(url).json()

    def find_descendant_names(self, concept: str) -> List[str]:
        names = list()
        ds = self.find_descendants(concept)
        if ds:
            VarsKnowledgebase.__accumulate_names([ds], names)
        return names

    @staticmethod
    def __accumulate_names(concepts: List[Dict], accum: List[str] = list()):
        for concept in concepts:
            accum.append(concept["name"])
            if 'children' in concept:
                VarsKnowledgebase.__accumulate_names(
                    concept["children"], accum)
