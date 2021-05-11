import backblaze
from backblaze.settings import PartSettings

from progress.bar import Bar
from os import path


FILE = "..."
BUCKET_ID = "..."
READ_SIZE = 5000000
KEY_ID = "..."
KEY = "..."
TIMEOUT = 900

CURRENT_PATH = path.dirname(path.realpath(__file__))
FILE_LOCATION = path.join(CURRENT_PATH, FILE)
FILE_SIZE = path.getsize(FILE_LOCATION)


b2 = backblaze.Blocking(
    KEY_ID,
    KEY,
    timeout=TIMEOUT
)


b2.authorize()


progress_bar = Bar("Total upload", max=FILE_SIZE)


with open(FILE_LOCATION, "rb") as f:
    _, file = b2.bucket(bucket_id=BUCKET_ID).create_part(
        PartSettings(FILE)
    )

    parts = file.parts()

    data = True
    while data:
        data = f.read(READ_SIZE)
        if data:
            parts.data(data)
            progress_bar.next(len(data))

    parts.finish()


progress_bar.finish()
