import os
import requests
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()
host_url = urljoin(os.getenv('READARR_AUDIOBOOK_URL'), 'api/v1/')
headers = {
    'x-api-key': os.getenv('READARR_AUDIOBOOK_APIKEY')
}

def search_audiobook(term):
    a = requests.get(f'{host_url}search/?term={term}', headers=headers)
    b = a.json()
    c = []
    for i in b:
        if 'book' in i:
            c.append(i['book'])
    return c

def add_audiobook(book):
    from connectors.common import get_data
    [root_dir, quality_profileid, metadata_profileid] = get_data("audiobook", host_url, headers)
    book["author"]["rootFolderPath"] = root_dir
    book["author"]["addOptions"] = {
        "monitor": "none",
        "searchForMissingBooks": False
    }
    book["author"]["qualityProfileId"] = quality_profileid
    book["author"]["metadataProfileId"] = metadata_profileid
    book["addOptions"] = {
        "searchForNewBook": True
    }
    book["manualAdd"] = True
    r = requests.post(f'{host_url}book', headers=headers, json=book)
    if r.status_code == 201:
        return f'Great success. The audiobook **{book["title"]}** has been added.'
    elif r.status_code == 409:
        return f'This audiobook is already in Readarr'
    else:
        return f'Unable to add audiobook due to error {r.status_code}'