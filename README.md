# Backblaze Asynchronous Wrapper
[Backblaze Documentation](https://www.backblaze.com/b2/docs)

## Notes
Our wrapper only adjusts the names for required inputs, e.g. if we wanted to use https://www.backblaze.com/b2/docs/b2_list_parts.html
```py
await b2_client.list.file_names(file_id="", startPartNumber="1", maxPartCount="100")
```

### Example
```py
import asyncio
import aiob2

b2_client = aiob2(application_key_id="", application_key="")

async def testing():
    print(await b2_client.list.file_names(bucket_id=""))

    await b2_client.session.close()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(testing())
loop.close()
```