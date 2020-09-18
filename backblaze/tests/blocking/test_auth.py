import unittest

from .shared_vars import CLIENT

from ...models.auth import AuthModel


class TestBlockingAuth(unittest.TestCase):
    def test_auth(self):
        self.assertTrue(
            type(CLIENT.authorize()) == AuthModel
        )

    def tearDown(self):
        CLIENT.close()
