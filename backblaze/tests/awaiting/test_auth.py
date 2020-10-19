import asynctest

from .client import CLIENT

from ...models.auth import AuthModel


class TestAwaitingAuth(asynctest.TestCase):
    use_default_loop = True

    async def test_auth(self):
        self.assertIsInstance(
            await CLIENT.authorize(), AuthModel
        )
