import unittest

from .client import CLIENT

from ...settings import KeySettings

from ...models.key import KeyModel

from ...key.blocking import BlockingKey


class TestKeyBlocking(unittest.TestCase):
    def test_key(self):
        created_data, created_key = CLIENT.create_key(KeySettings(
            ["listFiles"],
            "test key"
        ))

        self.assertIsInstance(
            created_data, KeyModel
        )

        self.assertIsInstance(
            created_key, BlockingKey
        )

        for data, key in CLIENT.keys():
            self.assertIsInstance(
                data, KeyModel
            )

            self.assertIsInstance(
                key, BlockingKey
            )

        self.assertIsInstance(
            created_key.delete(), KeyModel
        )
