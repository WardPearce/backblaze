import asynctest

from ...exceptions import AuthorizeRequired

from ... import Awaiting as AwaitingClient


class TestMiscBlocking(asynctest.TestCase):
    async def test_forgot_to_call_authorize(self):
        b2_client = AwaitingClient("", "")

        with self.assertRaises(AuthorizeRequired):
            await b2_client.download_by_name("", "")
