import os
import asyncio
import aiob2

from resources import B2, BUCKET_NAME


class BucketTest:
    async def _save_files(self):
        for counter in range(0, 4):
            file_name = "aiob2/test{}.bin".format(counter)

            print("Saving {} into {}".format(
                file_name,
                self.bucket.bucket_id
            ))

            await self.bucket.upload.data(
                data=b"c43f25647e967cecd5ea7f967ee3c1f9",
                file_name=file_name
            )

            print("Saved {}".format(file_name))

            await asyncio.sleep(0.001)

    async def delete(self):
        async for data, file in self.bucket.files.versions():
            print("Deleting file {}".format(data.file_name))

            await file.delete(data.file_name)

            print("Deleted file {}".format(data.file_name))

        print("Deleting bucket {}".format(self.bucket.bucket_id))

        await self.bucket.delete()

        print("Deleted bucket {}".format(self.bucket.bucket_id))

    async def run(self):
        try:
            bucket_ids = []
            buckets_append = bucket_ids.append
            async for data, _ in B2.buckets():
                buckets_append(
                    data.bucket_id
                )

            print("Current bucket IDs:\n {}".format(bucket_ids))

        except Exception as e:
            print(e)
        else:
            print("Creating {}".format(BUCKET_NAME))

            self.bucket = B2.bucket()

            await self.bucket.create(
                BUCKET_NAME,
                aiob2.bucket.models.BucketTypes.private
            )

            print("Created {}".format(BUCKET_NAME))

            await self._save_files()

            pathway = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "test_image.png"
            )
            if os.path.exists(pathway):
                print("Attempting to upload {}".format(pathway))

                await self.bucket.upload.file(
                    "aiob2/foobar.png",
                    pathway
                )

                print("Uploaded {}".format(pathway))

            print("Hiding test_image.png")

            await self.bucket.files.hide("aiob2/foobar.png")

            print("test_image.png is hidden")
