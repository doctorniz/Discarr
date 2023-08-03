import os
import requests
from dotenv import load_dotenv
from urllib.parse import urljoin

load_dotenv()
host_url = urljoin(os.getenv('LIDARR_URL'), 'api/v1/')
headers = {
    'x-api-key': os.getenv('LIDARR_APIKEY')
}

def get_quality_profile_id():
    a = requests.get(f'{host_url}qualityprofile', headers=headers)
    b = a.json()
    if os.getenv(f'LIDARR_QUALITY'):
        c = os.getenv(f'LIDARR_QUALITY')
    else:
        c = 'Any'
    for i in b:
        if i['name'] == c:
            return i['id']
    return 1

def get_metadata_profile_id():
    a = requests.get(f'{host_url}metadataprofile', headers=headers)
    b = a.json()
    if os.getenv(f'LIDARR_METADATA'):
        c = os.getenv(f'LIDARR_METADATA')
    else:
        c = 'Standard'
    for i in b:
        if i['name'] == c:
            return i['id']
    return 1

def search_album(term):
    a = requests.get(f'{host_url}album/lookup/?term={term}', headers=headers)
    b = a.json()
    return b

def add_album(album):
    from connectors.common import get_data
    [root_dir] = get_data("album", host_url, headers)
    quality_profile_id = get_quality_profile_id()
    metadata_profile_id = get_metadata_profile_id()

    album["artist"]["rootFolderPath"] = root_dir
    album["artist"]["qualityProfileId"] = quality_profile_id
    album["artist"]["metadataProfileId"] = metadata_profile_id
    album["artist"]["addOptions"] = {
            "monitor": "future",
            "searchForMissingAlbums": False,
        }
    album["monitored"] = True
    album["addOptions"] = {
            "searchForNewAlbum": True,
    }
    


    r = requests.post(f'{host_url}album', headers=headers, json=album)
    if r.status_code == 201:
        return f'Great success. The movie **{album["title"]}** has been added.'
    elif r.status_code == 409:
        return f'This album is already in Lidarr'
    else:
        print(r.text)
        return f'Unable to add album due to error {r.status_code}'