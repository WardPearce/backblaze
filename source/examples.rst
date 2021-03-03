Examples
========

Here are some simple examples on how to use this wrapper.
This is written using the blocking wrapper, but still applies to the awaiting wrapper.

Assume that "client" has been initialized & authorize has been called.


Creating a bucket
~~~~~~~~~~~~~~~~~
.. code-block:: python

    from backblaze.settings import BucketSettings


    data, bucket = client.create_bucket(BucketSettings(
        name="creating a bucket example",
        private=True
    ))


Listing buckets
~~~~~~~~~~~~~~~
.. code-block:: python

    for data, bucket in client.buckets():
        print(data.name)

        # Interact with the bucket.
        bucket.update(...)


Interacting with a bucket
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    bucket = client.bucket(bucket_id="...")

    # Interact with the bucket.
    bucket.update(...)


Uploading a file
~~~~~~~~~~~~~~~~
.. code-block:: python

    import os
    from backblaze.settings import UploadSettings


    bucket = client.bucket(bucket_id="...")

    local_path = os.path.join(
        os.path.dirname(path.realpath(__file__)),
        "/amazing_file.png"
    )

    # If the file is above 5mb, the file will be
    # uploaded in parts.
    data, file = bucket.upload_file(
        UploadSettings("kinda cool.png"),
        local_path
    )

Uploading parts
~~~~~~~~~~~~~~~
.. code-block:: python

    from backblaze.settings import PartSettings


    bucket = client.bucket(bucket_id="...")

    _, file = bucket.create_part(PartSettings(
        name="ウィーブ.jpg"
    ))

    parts = file.parts()
    parts.file(pathway="path/to/weeb/file.jpg")
    parts.finish()

Downloading
~~~~~~~~~~~
.. code-block:: python

    data = bucket.file(file_id="...").download()

Async download iterate
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    async for data in bucket.file(file_id="...").download_iterate():
        pass

Download by name
~~~~~~~~~~~~~~~~
.. code-block:: python

    data = client.download_by_name(bucket_name="...", file_name="foobar.jpg")
