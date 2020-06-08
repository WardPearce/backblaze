import hashlib
import aiofiles
import os

from .exceptions import NoSuchFile, InvalidPartNumber


def format_keys(given_dict):
    params = {}
    for key in given_dict:
        params[key.replace("__", "-")] = given_dict[key]

    return params


def part_number(number):
    if number > 10000 or number < 1:
        raise InvalidPartNumber()


def get_sha1(data):
    return hashlib.sha1(data).hexdigest()


async def read_file(file_pathway):
    if os.path.isfile(file_pathway):
        sha1 = hashlib.sha1()
        sha1_update = sha1.update

        contents = {
            "data": b"",
            "bytes": str(os.path.getsize(file_pathway)),
        }

        async with aiofiles.open(file_pathway, mode="rb") as f:
            async for line in f:
                sha1_update(line)
                contents["data"] += line

        contents["sha1"] = sha1.hexdigest()

        return contents

    raise NoSuchFile()
