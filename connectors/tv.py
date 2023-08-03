import os
import requests
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()
host_url = urljoin(os.getenv('SONARR_URL'), 'api/v3/')
headers = {
    'x-api-key': os.getenv('SONARR_APIKEY')
}

def search_series(term):
    a = requests.get(f'{host_url}series/lookup/?term={term}', headers=headers)
    b = a.json()
    return b

def add_series(series):
    from connectors.common import get_data
    [root_dir, quality_profile_id, language_profile_id] = get_data("tv", host_url, headers)

    series["rootFolderPath"] = root_dir
    series["qualityProfileId"] = quality_profile_id
    series["languageProfileId"] = language_profile_id
    series["monitored"] = True
    series["addOptions"] = {
        "ignoreEpisodesWithFiles": True,
        "ignoreEpisodesWithoutFiles": False,
        "searchForMissingEpisodes": True,
    }
    r = requests.post(f'{host_url}series', headers=headers, json=series)
    if r.status_code == 201:
        return f'Great success. The series **{series["title"]}** has been added.'
    elif r.status_code == 409 or r.status_code == 400:
        return f'This series is already in Sonarr'
    else:
        return f'Unable to add series due to error {r.status_code}'
