# Index
- [aiob2.bucket.files.hide](#async-aiob2bucketfileshide)
- [aiob2.bucket.files.versions](#async-aiob2bucketfilesversions)
- [aiob2.bucket.files.names](#async-aiob2bucketfilesnames)
- [aiob2.bucket.files.unfinished_large_files](#async-aiob2bucketfilesunfinished_large_files)
- [aiob2.bucket.files.download_authorization](#async-aiob2bucketfilesdownload_authorization)

### Bucket Files
___

##### async aiob2.bucket.files.hide

**Functionality**

Hides a file.


**Parameters**

- file_name: str
    - Name of file.

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

    upload = await bucket.files.hide(
        file_name="..."
    )
```

___

##### async aiob2.bucket.files.versions

**Functionality**

Lists versions.


**Parameters**

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

    async for data, file in bucket.files.versions():
        pass
```

___

##### async aiob2.bucket.files.names

**Functionality**

List file names.


**Parameters**

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

    async for data, file in bucket.files.names():
        pass
```

___

##### async aiob2.bucket.files.unfinished_large_files

**Functionality**

List unfinished large files.


**Parameters**

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

    async for data, file in bucket.files.unfinished_large_files():
        pass
```

___

##### async aiob2.bucket.files.download_authorization

**Functionality**

Used to generate an authorization token that can be used to download files with the specified prefix.


**Parameters**

- **kwargs

**Response**

- GetDowloadAuthModel

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    bucket = B2.bucket(
        bucket_id="..."
    )

    auth = await bucket.files.unfinished_large_files()
```

___