import os
from pathlib import Path
import requests

from dotenv import load_dotenv


def download_file(file_url, file_path):
    file_path = Path(file_path)
    Path(file_path.parent).mkdir(parents=True, exist_ok=True)
    response = requests.get(file_url, verify=False)
    response.raise_for_status()
    file_path.write_bytes(response.content)


def find_filename_in_url(url):
    filename_start_index = url.rindex("/") + 1
    return url[filename_start_index:]


def fetch_xkcd_comic(comic_id):
    comic_url = f"http://xkcd.com/{comic_id}/info.0.json"
    comic_response = requests.get(comic_url)
    comic_response.raise_for_status()
    comic = comic_response.json()
    comic_image_url = comic["img"]
    comic_comment = comic["alt"]
    image_name = find_filename_in_url(comic_image_url)
    download_file(comic_image_url, image_name)
    print(comic_comment)


def get_test_vk_response(access_token):
    method_name = "groups.get"
    vk_api_url = f"https://api.vk.com/method/{method_name}"
    request_parameters = {
        "access_token": access_token,
        "v": "5.126",
        "extended": 1,
        "fields": "name",
    }
    vk_groups_response = requests.get(vk_api_url, params=request_parameters)
    vk_groups_response.raise_for_status()
    return vk_groups_response.json()


if __name__ == "__main__":
    load_dotenv()
    vk_access_token = os.getenv("VK_ACCESS_TOKEN")
    print(get_test_vk_response(vk_access_token))

    # fetch_xkcd_comic(355)
