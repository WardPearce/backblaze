# Index


##### async aiob2.file.parts.upload.get

**Functionality**

Gets upload url for part.


**Parameters**

None

**Response**

- GetUploadUrlModel

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    file = B2.file(
        file_id="..."
    )

    url = await file.parts.upload.get()
```

___

##### async aiob2.file.parts.upload.data

**Functionality**

Uploads a part of data.

**Parameters**

- data: bytes
    - Data to upload.
- bytes_count: int
    - amount of bytes
- x_bz_part_number: int
    - A number from 1 to 10000. The parts uploaded for one file must have contiguous numbers, starting with 1.

**Response**

- PartModel

**Raises**

- Can raise any request related exception.
- InvalidPartNumber

**Example**

```python
async def example():
    file = B2.file(
        file_id="..."
    )

    await file.parts.upload.get()
```

___

##### async aiob2.file.parts.upload.cancel

**Functionality**

Cancels part upload.

**Parameters**

None

**Response**

- PartDeleteModel
- Bucket

**Raises**

- Can raise any request related exception.

**Example**

```python
async def example():
    file = B2.file(
        file_id="..."
    )

    await file.parts.upload.cancel()
```

___
