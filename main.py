import os
from random import randint

import requests
from dotenv import load_dotenv

from xkcd_utils import get_number_xkcd_comics
from vk_utils import post_comic_on_vk_wall


def main():
    load_dotenv()
    vk_access_token = os.getenv("VK_ACCESS_TOKEN")
    vk_group_id = os.getenv("VK_GROUP_ID")
    number_of_comics = get_number_xkcd_comics()
    random_comic_id = randint(1, number_of_comics)
    api_version = "5.126"
    try:
        post_comic_on_vk_wall(vk_access_token, api_version, vk_group_id,
                              random_comic_id)
    except requests.exceptions.HTTPError as error:
        print(error)


if __name__ == "__main__":
    main()
