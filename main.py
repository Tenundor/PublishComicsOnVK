from pathlib import Path
import requests


def download_file(file_url, file_path):
    file_path = Path(file_path)
    Path(file_path.parent).mkdir(parents=True, exist_ok=True)
    response = requests.get(file_url, verify=False)
    response.raise_for_status()
    file_path.write_bytes(response.content)


def find_filename_in_url(url):
    filename_start_index = url.rindex("/")
    return url[filename_start_index + 1:]


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


if __name__ == "__main__":
    fetch_xkcd_comic(150)
