from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests


def download_file(file_url, filename):
    filename = Path(filename)
    response = requests.get(file_url, verify=False)
    response.raise_for_status()
    filename.write_bytes(response.content)


def request_xkcd_comic(comic_id=""):
    comic_url = f"http://xkcd.com/{comic_id}/info.0.json"
    comic_response = requests.get(comic_url)
    comic_response.raise_for_status()
    return comic_response.json()


def fetch_xkcd_comic(comic_id):
    comic = request_xkcd_comic(comic_id)
    comic_url = comic["img"]
    comic_comment = comic["alt"]
    comic_path = unquote(urlsplit(comic_url).path)
    image_name = comic_path[comic_path.rindex("/") + 1:]
    download_file(comic_url, image_name)
    return {
        "filename": image_name,
        "comment": comic_comment,
    }
