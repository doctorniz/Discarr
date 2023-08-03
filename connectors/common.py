import requests
import os

def get_data(type, host_url, headers):
    if type in ["book", "audiobook"]:
        return [
            get_root_dir(host_url, headers), 
            get_quality_profileid(host_url, headers, f'READARR_{type.upper()}'), 
            get_metadata_profileid(host_url, headers, f'READARR_{type.upper()}')
            ]
    elif type =="movie":
        return [
            get_root_dir(host_url, headers),
            get_quality_profileid_tv(host_url, headers, f'RADARR'),
        ]
    elif type == "tv":
        return [
            get_root_dir(host_url, headers),
            get_quality_profileid_tv(host_url, headers, f'SONARR'),
            1
        ]
    elif type == "album":
        return [
            get_root_dir(host_url, headers)        ]

def get_root_dir(host_url, headers):
    a = requests.get(f'{host_url}rootfolder', headers=headers)
    b = a.json()
    c = b[0]['path']
    return c

def get_quality_profileid(host_url, headers, pre):
    if os.getenv(f'{pre}_QUALITYPROFILEID'):
        return int(os.getenv(f'{pre}_QUALITYPROFILEID'))
    else:
        a = requests.get(f'{host_url}qualityprofile', headers=headers)
        b = a.json()
        return b[0]["id"]

def get_quality_profileid_tv(host_url, headers, pre):
    a = requests.get(f'{host_url}qualityprofile', headers=headers)
    b = a.json()
    if os.getenv(f'{pre}_QUALITY'):
        c = os.getenv(f'{pre}_QUALITY')
    else:
        c = 'HD-1080p'
    for i in b:
        if i['name'] == c:
            return i['id']
    return 1

def get_metadata_profileid(host_url, headers, pre):
    if os.getenv(f'{pre}_METADATAPROFILEID'):
        return int(os.getenv(f'{pre}_METADATAPROFILEID'))
    else:
        a = requests.get(f'{host_url}metadataprofile', headers=headers)
        b = a.json()
        return b[0]["id"]