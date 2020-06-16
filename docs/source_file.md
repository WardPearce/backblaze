### Source File
___

##### aiob2.source_file.copy.part

**Functionality**

Copies from an existing B2 file, storing it as a part of a large file which has already been started.


**Parameters**

- large_file_id
- part_number
- **kwargs

**Response**

- PartModel
- File

**Raises**

- Can raise any request related exception.
- InvalidPartNumber

**Example**

```python
async def example():
    source_file = B2.source_file(
        source_file_id="..."
    )

    data, file = await source_file.copy.part(
        large_file_id="...",
        part_number=0,
    )
```

___

##### aiob2.source_file.copy.file

**Functionality**

When calling b2_copy_file, by default the entire source file will be copied to the destination.


**Parameters**

- file_name
- **kwargs

**Response**

- FileModel
- File

**Raises**

- Can raise any request related exception.

**Example**

```python
async def example():
    source_file = B2.source_file(
        source_file_id="..."
    )

    data, file = await source_file.copy.file(
        file_name="..."
    )
```

___