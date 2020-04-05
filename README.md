##### Version 0.1.0 is NOT backwards compatibility with anything below that version.

## Install 
Install git and run ``pip3 install git+https://github.com/WardPearce/aiob2.git``

## Notes
- Our wrapper only adjusts the names for required inputs, any non-required input what uses a '-' replace it with '__'.
- Don't start a pathway with a '/'.

## Index
- [Backblaze Docs](https://www.backblaze.com/b2/docs/)
- [API](#api)
- [Example](#example)

## API
##### aiob2.client
``aiob2.client(application_key_id, application_key, session=None, debug=False)``
- If you aren't passing a aiohttp.ClientSession object created within the event loop aiob2.client should be ran within the context of the loop.

##### aiob2.client(...).bucket(self, bucket_id)
    - delete(self)
        Delete the given bucket.

    - file
        - hide(self, file_name)
            Hides a file so that downloading by name will not find the file.
        - versions(self, **kwargs)
            Lists all of the versions of all of the files.
        - names(self, **kwargs)
            Lists the names of all files in a bucket.
        - download_authorization(self, file_name_prefix, valid_duration_in_seconds, **kwargs)
            Used to generate an authorization token that can be used to download files.
        - unfinished_large_files(self, **kwargs)
            Lists information about large file uploads that have been started.

    - upload
        - get(self)
            Gets an URL to use for uploading files.
        - file(self, file_name, file_pathway, content_type="b2/x-auto", **kwargs)
            Used to upload local files onto the bucket, returning its unique file ID.
        - data(self, data, file_name, content_type="b2/x-auto", **kwargs)
            Used to upload data in memory onto the bucket, returning its unique file ID.

##### aiob2.client(...).account
    - create
        - key(self, capabilities, key_name, **kwargs)
            Creates a new application key.
        - bucket(self, bucket_name, bucket_type, **kwargs)
            Creates a new bucket. A bucket belongs to the account used to create it.
    
    - list
        - keys(self, **kwargs)
            Lists application keys associated with an account.
        - buckets(self, **kwargs)
            Lists buckets associated with an account, in alphabetical order by bucket name.

##### aiob2.client(...).file(self, file_id=None)
    - info(self)
        Gets information about one file stored in B2.
    - finish(self, part_sha1_array)
        Converts the parts that have been uploaded into a single B2 file.
    - download(self)
        Downloads one file from B2.
    - parts(self, **kwargs)
        Lists the parts that have been uploaded for a large file that has not been finished yet.
    
    - upload
        - get(self)
            Gets an URL to use for uploading parts of a large file.
        - part(self, data, bytes_count, x_bz_part_number: int)
            Uploads one part of a large file to B2.
        - cancel(self)
            Cancels the upload of a large file, and deletes all of the parts that have been uploaded.

##### aiob2.client(...).source_file(self, source_file_id)
    - copy
        - part(self, large_file_id, part_number, **kwargs)
            Copies from an existing B2 file.
        - file(self, file_name, **kwargs)
            Creates a new file by copying from an existing file.

## Example
```py
import asyncio
import aiob2

async def example():
    b2 = aiob2.client(application_key="....", application_key_id="....")

    print(await b2.bucket(bucket_id="33e138c438fbe35e6be90b11").upload.data(data=b"world", file_name="test/hello.txt"))

    await b2.session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(example())
loop.close()
```