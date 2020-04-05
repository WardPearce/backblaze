Simple asynchronous wrapper for Backblaze B2 with 100% coverage.

## Install 
Install git and run pip3 ``install git+https://github.com/WardPearce/aiob2.git``

## Notes
Our wrapper only adjusts the names for required inputs, any input what uses a '.' replace it with '__'.

## API
##### aiob2.client
``aiob2.client(application_key_id, application_key, session=None, debug=False)``
- If you aren't passing a aiohttp.ClientSession object created within the event loop aiob2.client should be ran within the context of the loop.

##### aiob2.client(...).bucket(self, bucket_id)
    - delete(self)
        Delete the given bucket.

    - file(self)
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

    - upload(self)
        - get(self)
            Gets an URL to use for uploading files.
        - file(self, file_name, file_pathway, content_type="b2/x-auto", **kwargs)
            Used to upload local files onto the bucket, returning its unique file ID.
        - data(self, data, file_name, content_type="b2/x-auto", **kwargs)
            Used to upload data in memory onto the bucket, returning its unique file ID.