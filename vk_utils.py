import os

import requests


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
        raise requests.exceptions.HTTPError(error["error_msg"])
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


def post_comic_on_vk_wall(access_token, api_version, group_id, comic):
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
    os.remove(comic["filename"])
    return api_response_post

