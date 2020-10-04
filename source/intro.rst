Intro
=====
This wrapper has both asynchronous & synchronous support, this intro will cover the basic of both.
Lucily for you the API for asynchronous (awaiting) & synchronous (blocking) is identical.


Getting started
---------------

**Awaiting**

.. code-block:: python

    import backblaze

    client = backblaze.Awaiting(
        key_id="...",
        key="..."
    )

    # A client should always be closed after being used!
    await client.close()


**Blocking**

.. code-block:: python

    import backblaze

    client = backblaze.Blocking(
        key_id="...",
        key="..."
    )

    # A client should always be closed after being used!
    client.close()
