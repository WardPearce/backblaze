# Index
- [aiob2.client](#aiob2client)
- [aiob2.client.connect](#async-aiob2clientconnect)
- [aiob2.client.close](#async-aiob2clientclose)
- [aiob2.client.bucket](#aiob2clientbucket)
- [aiob2.client.source_file](#aiob2clientsource_file)
- [aiob2.client.file](#aiob2clientfile)

### Client
___

##### aiob2.client

**Functionality**

Used to communicate to Backblaze's B2 API.


**Parameters**

- key_id: str
    API Key ID.
- application_key: str
    API App Key.
- max_cache: int
    Max amount of upload urls allowed to be cached at a given time.
- chunk_size: int
    How many chunks should we read each loop.

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
    Optionally pass your own aiohttp.ClientSession.

**Response**

None

**Raises**

- InvalidAuthorization
    Given Key ID & App Key wasn't valid.

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

##### aiob2.client.bucket

[Bucket documentation](/docs/bucket.md)

___

##### aiob2.client.source_file

[Source file documentation](/docs/source_file.md)

___

##### aiob2.client.file

[File documentation](/docs/file.md)

___