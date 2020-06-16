# Index
- [aiob2.bucket.create](#async-aiob2bucketcreate)
- [aiob2.bucket.delete](#async-aiob2bucketdelete)
- [aiob2.bucket.upload](#aiob2bucketupload)
- [aiob2.bucket.files](#aiob2bucketfiles)

### Bucket
___

##### async aiob2.bucket.create

**Functionality**

Creates a bucket and sets the initialized bucket object's ID to the created bucket's ID.


**Parameters**

- name: str
    - Unique name of bucket.
- type: BucketTypes
    - BucketTypes object.
- **kwargs

**Response**

- BucketModel

**Raises**

- Can raise any request related exception. 

**Example**

```python
from aiob2.bucket.models import BucketTypes

async def example():
    bucket = await B2.bucket.create(
        name="...",
        type=BucketTypes.private
    )
```

___

##### async aiob2.bucket.delete

**Functionality**

Deletes current bucket.


**Parameters**

None

**Response**

- BucketModel

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    bucket = B2.bucket(
        bucket_id="..."
    )

    await bucket.delete()
```

___

##### aiob2.bucket.upload

[Bucket upload documentation](/docs/bucket_upload.md)
___

##### aiob2.bucket.files

[Bucket files documentation](/docs/bucket_files.md)
___