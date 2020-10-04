Intro
=====
This wrapper has both asynchronous & synchronous support, this intro will cover the basic of both.
Lucily for you the API for asynchronous (awaiting) & synchronous (blocking) is identical.

Application keys can be made `here <https://secure.backblaze.com/app_keys.htm>`_.

Using '_' correctly is important, this wrapper uses Tuple's for returns.
For any variable what's return what you don't need use '_'. 


Getting started
---------------

**Awaiting**

This module uses asyncio's tasks to quietly update authentication. This requires python 3.7 or above.

.. code-block:: python

    import backblaze

    client = backblaze.Awaiting(
        key_id="...",
        key="..."
    )

    # Must be called before issuing any requests.
    await client.authorize()

    # A client should always be closed after being used!
    await client.close()


**Blocking**

This module uses threading to quietly update authentication.

.. code-block:: python

    import backblaze

    client = backblaze.Blocking(
        key_id="...",
        key="..."
    )

    # Must be called before issuing any requests.
    client.authorize()

    # Python's garbage collector should
    # close connections correctly for Blocking.
    client.close()
