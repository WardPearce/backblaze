# Index

##### async aiob2.file.parts.finish

**Functionality**

Gets info about a file.


**Parameters**

- part_sha1_array: str

**Response**

- FileModel
- Bucket

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    file = B2.file(
        file_id="..."
    )

    data, bucket = await file.finish(
        part_sha1_array="..."
    )
```

___

##### async aiob2.file.parts.list

**Functionality**

Lists all parts for given file.


**Parameters**

- **kwargs

**Response**

- PartModel

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    file = B2.file(
        file_id="..."
    )

    async for data in file.parts.list():
        pass
```

___

##### aiob2.client.file.parts.upload

[Parts upload documentation](/docs/file_parts_upload.md)