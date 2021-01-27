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


def request_xkcd_comic(comic_id=None):
    comics_host = "http://xkcd.com"
    if comic_id:
        comic_url = f"{comics_host}/{comic_id}/info.0.json"
    else:
        comic_url = f"{comics_host}/info.0.json"
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


def get_number_xkcd_comics():
    comic = request_xkcd_comic()
    return comic["num"]


def prepare_vk_api_url(method_name):
    return f"https://api.vk.com/method/{method_name}"


def send_vk_post_request(access_token, api_version, request_url,
                         file_type="photo", file=None, **payload):
    file_to_send = None
    if file:
        file_to_send = {
            file_type: file
        }
    payload.update({
        "access_token": access_token,
        "v": api_version,
    })
    response = requests.post(request_url, data=payload, files=file_to_send)
    response.raise_for_status()
    response_content = response.json()
    error = response_content.get("error")
    if error:
        raise requests.exceptions.HTTPError(error)
    return response_content


def get_vk_url_to_upload_photo(access_token, api_version, group_id):
    api_url = prepare_vk_api_url("photos.getWallUploadServer")
    response = send_vk_post_request(access_token, api_version, api_url,
                                    group_id=group_id)
    return response["response"]["upload_url"]


def upload_photo_to_vk(access_token, api_version, url_to_upload, filename):
    with open(filename, "rb") as photo:
        response = send_vk_post_request(access_token, api_version,
                                        url_to_upload, file=photo)
        return response


def save_vk_wall_photo(access_token, api_version, upload_api_response,
                       group_id=None, **save_parameters):
    save_parameters.update(upload_api_response)
    method_name = "photos.saveWallPhoto"
    api_url = prepare_vk_api_url(method_name)
    response = send_vk_post_request(access_token, api_version, api_url,
                                    group_id=group_id, **save_parameters)
    return response


def post_photo_on_wall(access_token, api_version, photo_id, photo_owner_id,
                       wall_owner_id, message="", friends_only=0, from_group=1,
                       **post_parameters):
    attachment = f"photo{photo_owner_id}_{photo_id}"
    method_name = "wall.post"
    api_url = prepare_vk_api_url(method_name)
    post_parameters.update({
        "owner_id": wall_owner_id,
        "friends_only": friends_only,
        "from_group": from_group,
        "message": message,
        "attachments": attachment,
    })
    response = send_vk_post_request(access_token, api_version, api_url,
                                    **post_parameters)
    return response


def post_comic_on_vk_wall(access_token, api_version, group_id, comic_id):
    comic = fetch_xkcd_comic(comic_id)
    url_to_upload = get_vk_url_to_upload_photo(access_token, api_version,
                                               group_id)
    api_response_upload = upload_photo_to_vk(access_token, api_version,
                                             url_to_upload, comic["filename"])
    api_response_save = save_vk_wall_photo(access_token, api_version,
                                           api_response_upload, group_id)
    api_response_save = api_response_save["response"][0]
    photo_id = api_response_save["id"]
    photo_owner_id = api_response_save["owner_id"]
    group_owner_id = -int(group_id)
    api_response_post = post_photo_on_wall(access_token, api_version,
                                           photo_id, photo_owner_id,
                                           group_owner_id, comic["comment"])
    return api_response_post


def main():
    load_dotenv()
    vk_access_token = os.getenv("VK_ACCESS_TOKEN")
    vk_group_id = os.getenv("VK_GROUP_ID")
    xkcd_comic_id = 1
    api_version = "5.126"
    response = post_comic_on_vk_wall(vk_access_token, api_version, vk_group_id,
                                     xkcd_comic_id)
    print(response)


if __name__ == "__main__":
    main()
