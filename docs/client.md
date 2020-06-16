# Index
- [aiob2.client](#aiob2client)
- [aiob2.client.connect](#async-aiob2clientconnect)
- [aiob2.client.close](#async-aiob2clientclose)
- [aiob2.client.keys](#async-aiob2clientkeys)
- [aiob2.client.buckets](#async-aiob2clientbuckets)
- [aiob2.client.download_from_name](#async-aiob2clientdownload_from_name)
- [aiob2.client.download_from_name_iterate](#async-aiob2clientdownload_from_name_iterate)
- [aiob2.client.bucket](#aiob2clientbucket)
- [aiob2.client.source_file](#aiob2clientsource_file)
- [aiob2.client.file](#aiob2clientfile)
- [aiob2.client.key](#aiob2clientkey)

### Client
___

##### aiob2.client

**Functionality**

Used to communicate to Backblaze's B2 API.


**Parameters**

- key_id: str
    - API Key ID.
- application_key: str
    - API App Key.
- max_cache: int
    - Max amount of upload urls allowed to be cached at a given time.
- chunk_size: int
    - How many chunks should we read each loop.

**Response**

None

**Raises**

None

**Example**

```python
import aiob2

# Rest of the examples will assume the client
# is stored under a variable called B2.
B2 = aiob2.client(key_id="...", application_key="...")
```

___

##### async aiob2.client.connect

**Functionality**

Gets authorization details needed to send requests.


**Parameters**

- session: aiohttp.ClientSession
    - Optionally pass your own aiohttp.ClientSession.

**Response**

None

**Raises**

- InvalidAuthorization
    - Given Key ID & App Key wasn't valid.

**Example**

```python
async def startup():
    await B2.connect()
```

___

##### async aiob2.client.close

**Functionality**

Closes the aiohttp.ClientSession.


**Parameters**

None

**Response**

None

**Raises**

None

**Example**

```python
async def shutdown():
    await B2.close()
```

___

##### async aiob2.client.keys

**Functionality**

Lists all keys.


**Parameters**

- **kwargs

**Response**

- KeyModel
- Bucket

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    
    async for data, bucket in B2.keys():
        pass
```

___

##### async aiob2.client.buckets

**Functionality**

Lists all buckets.


**Parameters**

- **kwargs

**Response**

- BucketModel
- Bucket

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    
    async for data, bucket in B2.buckets():
        pass
```

___

##### async aiob2.client.download_from_name

**Functionality**

Downloads the whole file into memory from name.


**Parameters**

- bucket_name: str
- file_name: str

**Response**

- Bytes

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    
    data = await B2.download_from_name(
        bucket_name="...",
        file_name="..."
    )
```

___

##### async aiob2.client.download_from_name_iterate

**Functionality**

Loops over the downloaded file.


**Parameters**

- bucket_name: str
- file_name: str

**Response**

- Bytes

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():

    async for data in B2.download_from_name_iterate(bucket_name="...", file_name="..."):
        pass
```

___

##### aiob2.client.bucket

**Parameters**

- bucket_id
    - Unique bucket ID.

[Bucket documentation](/docs/bucket.md)

___

##### aiob2.client.source_file

**Parameters**

- source_file_id
    - Unique source file ID.

[Source file documentation](/docs/source_file.md)

___

##### aiob2.client.file

**Parameters**

- file_id
    - Unique file ID.

[File documentation](/docs/file.md)

___

##### aiob2.client.key

[Key documentation](/docs/key.md)

___