from aiob2 import b2

assert b2

if __name__ == "__main__":
    import asyncio

    b2_client = b2(application_key_id="", application_key="", debug=True)

    async def testing():
        print(await b2_client.list.file_names(bucket_id="33e138c438fbe35e6be90b11"))

        await b2_client.session.close()
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing())
    loop.close()