from resources import B2, SHARD_VARS

import os


class FileTest:
    async def run(self):
        file = B2.file(SHARD_VARS.file_id)

        print("Attempting to download {}".format(SHARD_VARS.file_id))

        print(await file.download())

        print("Attempting to smartly download the same file")

        async for data in file.download_iterate():
            print(data)

        pathway = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "{}.bin".format(SHARD_VARS.file_id)
        )

        print("Attempting to save the file to {}".format(pathway))

        await file.save(pathway)

        print("Completed")
