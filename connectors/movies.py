import os
import requests
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()
host_url = urljoin(os.getenv('RADARR_URL'), 'api/v3/')
headers = {
    'x-api-key': os.getenv('RADARR_APIKEY')
}

def search_movie(term):
    a = requests.get(f'{host_url}movie/lookup/?term={term}', headers=headers)
    b = a.json()
    return b

def add_movie(movie):
    from connectors.common import get_data
    [root_dir, quality_profile_id] = get_data("movie", host_url, headers)

    movie["rootFolderPath"] = root_dir
    movie["qualityProfileId"] = quality_profile_id
    movie["monitored"] = True
    movie["addOptions"] = {
        "monitor": 'movieAndCollection',
        "searchForMovie": True,
    }

    r = requests.post(f'{host_url}movie', headers=headers, json=movie)
    
    if r.status_code == 201:
        return f'Great success. The movie **{movie["title"]}** has been added.'
    elif r.status_code == 409:
        return f'This movie is already in Radarr'
    else:
        return f'Unable to add movie due to error {r.status_code}'



