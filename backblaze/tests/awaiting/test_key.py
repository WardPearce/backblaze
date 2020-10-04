import asynctest

from .client import CLIENT

from ...settings import KeySettings

from ...models.key import KeyModel

from ...key.awaiting import AwaitingKey


class TestKeyAwaiting(asynctest.TestCase):
    use_default_loop = True

    async def test_key(self):
        created_data, created_key = await CLIENT.create_key(KeySettings(
            ["listFiles"],
            "test key"
        ))

        self.assertIsInstance(
            created_data, KeyModel
        )

        self.assertIsInstance(
            created_key, AwaitingKey
        )

        async for data, key, _ in CLIENT.keys():
            self.assertIsInstance(
                data, KeyModel
            )

            self.assertIsInstance(
                key, AwaitingKey
            )

        self.assertIsInstance(
            await created_key.delete(), KeyModel
        )
