from pathlib import Path

import requests


def download_file(file_url, filename):
    filename = Path(filename)
    response = requests.get(file_url, verify=False)
    response.raise_for_status()
    filename.write_bytes(response.content)


def find_filename_in_url(url):
    filename_start_index = url.rindex("/") + 1
    return url[filename_start_index:]


def request_xkcd_comic(comic_id=""):
    comic_url = f"http://xkcd.com/{comic_id}/info.0.json"
    comic_response = requests.get(comic_url)
    comic_response.raise_for_status()
    return comic_response.json()


def fetch_xkcd_comic(comic_id):
    comic = request_xkcd_comic(comic_id)
    comic_image_url = comic["img"]
    comic_comment = comic["alt"]
    image_name = find_filename_in_url(comic_image_url)
    download_file(comic_image_url, image_name)
    return {
        "filename": image_name,
        "comment": comic_comment,
    }
