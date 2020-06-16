# Index
- [InvalidAuthorization](#aiob2exceptionsinvalidauthorization)
- [NoSuchFile](#aiob2exceptionsnosuchfile)
- [InvalidPartNumber](#aiob2exceptionsinvalidpartnumber)
- [BadRequest](#aiob2exceptionsbadrequest)
- [Forbidden](#aiob2exceptionsforbidden)
- [RequestTimeout](#aiob2exceptionsrequesttimeout)
- [TooManyRequests](#aiob2exceptionstoomanyrequests)
- [InternalError](#aiob2exceptionsinternalerror)
- [ServiceUnavailable](#aiob2exceptionsserviceunavailable)
- [UndefinedError](#aiob2exceptionsundefinederror)

### Exceptions
___

##### aiob2.exceptions.InvalidAuthorization

**Parameters**

None

**Functionality**

Raised when authorization is invalid.

**Response**

None

**Raises**

- InvalidAuthorization

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.InvalidAuthorization()
except aiob2.exceptions.InvalidAuthorization:
    pass
```

___

##### aiob2.exceptions.NoSuchFile

**Parameters**

None

**Functionality**

Raised when file doesn't exist.

**Response**

None

**Raises**

- NoSuchFile

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.NoSuchFile()
except aiob2.exceptions.NoSuchFile:
    pass
```

___

##### aiob2.exceptions.InvalidPartNumber

**Parameters**

None

**Functionality**

Raised when a part number is above / below 1,000 / 0.

**Response**

None

**Raises**

- InvalidPartNumber

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.InvalidPartNumber()
except aiob2.exceptions.InvalidPartNumber:
    pass
```

___

##### aiob2.exceptions.BadRequest

**Parameters**

None

**Functionality**

Raised when a bad request is sent.

**Response**

None

**Raises**

- BadRequest

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.BadRequest()
except aiob2.exceptions.BadRequest:
    pass
```

___

##### aiob2.exceptions.Forbidden

**Parameters**

None

**Functionality**

Raised when a forbidden request is made.

**Response**

None

**Raises**

- Forbidden

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.Forbidden()
except aiob2.exceptions.Forbidden:
    pass
```


___

##### aiob2.exceptions.RequestTimeout

**Parameters**

None

**Functionality**

Raised when a request timeouts. Note this is only when Backblaze times out & not aiohttp.

**Response**

None

**Raises**

- RequestTimeout

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.RequestTimeout()
except aiob2.exceptions.RequestTimeout:
    pass
```


___

##### aiob2.exceptions.TooManyRequests

**Parameters**

None

**Functionality**

Raised when too many requests are being sent (i.e. rate limiting).

**Response**

None

**Raises**

- TooManyRequests

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.TooManyRequests()
except aiob2.exceptions.TooManyRequests:
    pass
```


___

##### aiob2.exceptions.InternalError

**Parameters**

None

**Functionality**

Raised when something errors on Backblaze's side.

**Response**

None

**Raises**

- InternalError

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.InternalError():
except aiob2.exceptions.InternalError:
    pass
```


___

##### aiob2.exceptions.ServiceUnavailable

**Parameters**

None

**Functionality**

Raised when the service is temporarily unavailable.

**Response**

None

**Raises**

- ServiceUnavailable

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.ServiceUnavailable()
except aiob2.exceptions.ServiceUnavailable:
    pass
```


___

##### aiob2.exceptions.UndefinedError

**Parameters**

None

**Functionality**

Raised when Backblaze gives us a status code this wrapper doesn't understand.

**Response**

None

**Raises**

- UndefinedError

**Example**

```python
import aiob2

try:
    raise aiob2.exceptions.UndefinedError()
except aiob2.exceptions.UndefinedError:
    pass
```


___