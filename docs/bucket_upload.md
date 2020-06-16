# Index
- [aiob2.bucket.upload.get](#async-aiob2bucketuploadget)
- [aiob2.bucket.upload.file](#async-aiob2bucketuploadfile)
- [aiob2.bucket.upload.data](#async-aiob2bucketuploaddata)

### Bucket Upload
___

##### async aiob2.bucket.upload.get

**Functionality**

Gets a new upload url.


**Parameters**

None

**Response**

- GetUploadUrlModel

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    bucket = B2.bucket(
        bucket_id="..."
    )

    upload = await bucket.upload.get()
```

___

##### async aiob2.bucket.upload.file

**Functionality**

Uploads a local file onto B2.


**Parameters**

- file_name: str
    - Name to save the file under.
- pathway: str
    - Pathway to local file.
- content_type="b2/x-auto"
- **kwargs

**Response**

- FileModel
- File

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    bucket = B2.bucket(
        bucket_id="..."
    )

    data, file = await bucket.upload.file(
        file_name="hentai/foobar.png",
        pathway="foobar/something_cool.png"
    )
```

___

##### async aiob2.bucket.upload.data

**Functionality**

Uploads raw bytes onto B2.


**Parameters**

- data: bytes
    - Data to upload.
- file_name: str
    - Name to save the file under.
- content_type="b2/x-auto"
- **kwargs

**Response**

- FileModel
- File

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    bucket = B2.bucket(
        bucket_id="..."
    )

    data, file = await bucket.upload.data(
        data=b"wow",
        file_name="school_work/foobar.png"
    )
```

___