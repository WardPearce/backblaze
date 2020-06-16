# Index

### File
___

##### async aiob2.file.delete

**Functionality**

Deletes the given file.


**Parameters**

- file_name: str
    - Pathway / name of file.

**Response**

- FileDeleteModel

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    file = B2.file(
        file_id="..."
    )

    await file.delete(
        file_name="..."
    )
```

___

##### async aiob2.file.info

**Functionality**

Gets info about a file.


**Parameters**

None

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

    data, bucket = await file.info()
```

___

##### async aiob2.file.save

**Functionality**

Save's file to given local pathway.


**Parameters**

- pathway: str
    - Local pathway to save to

**Response**

None

**Raises**

- Can raise any request related exception.
- Can raise any aiofiles exception.

**Example**

```python
async def example():
    file = B2.file(
        file_id="..."
    )

    await file.save(
        pathway="..."
    )
```

___

##### async aiob2.file.download

**Functionality**

Downloads the whole file into memory.


**Parameters**

None

**Response**

None

**Raises**

- Can raise any request related exception.

**Example**

```python
async def example():
    file = B2.file(
        file_id="..."
    )

    data = await file.download()
```

___

##### async aiob2.file.download_iterate

**Functionality**

Iterate over downloaded file.


**Parameters**

None

**Response**

None

**Raises**

- Can raise any request related exception.

**Example**

```python
async def example():
    file = B2.file(
        file_id="..."
    )

    async for data in file.download_iterate():
        print(data)
```

___

##### aiob2.client.file.parts

[Parts documentation](/docs/file_parts.md)
