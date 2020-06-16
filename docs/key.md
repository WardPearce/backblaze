# Index


##### async aiob2.key.create

**Functionality**

Creates a key.


**Parameters**

- capabilities: list
- key_name: str
- **kwargs

**Response**

- KeyModel
- Bucket

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    key = await B2.key.create(
        capabilities=[],
        key_name="nice"
    )
```

___

##### async aiob2.key.delete

**Functionality**

Creates a key.


**Parameters**

- application_key_id: str

**Response**

- KeyModel
- Bucket

**Raises**

- Can raise any request related exception. 

**Example**

```python
async def example():
    key = await B2.key.delete(
        application_key_id="..."
    )
```

___