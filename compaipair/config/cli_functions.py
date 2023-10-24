import os

from compaipair.utils import get_cache_path, get_api_key


def print_cache_location():
    print(get_cache_path())


def save_api_key(api_key: str):
    with open(os.path.join(get_cache_path(), "api_key"), "w") as f:
        f.write(api_key)


def show_api_key():
    print(get_api_key())
