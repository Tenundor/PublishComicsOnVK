import os
from random import randint

from dotenv import load_dotenv
import requests

from vk_utils import post_comic_on_vk_wall
from xkcd_utils import fetch_xkcd_comic, request_xkcd_comic


def main():
    load_dotenv()
    vk_access_token = os.getenv("VK_ACCESS_TOKEN")
    vk_group_id = os.getenv("VK_GROUP_ID")
    number_of_comics = request_xkcd_comic()["num"]
    random_comic_id = randint(1, number_of_comics)
    api_version = "5.126"
    try:
        comic = fetch_xkcd_comic(random_comic_id)
        post_comic_on_vk_wall(vk_access_token, api_version, vk_group_id,
                              comic)
    except requests.exceptions.HTTPError as error:
        print(error)


if __name__ == "__main__":
    main()
