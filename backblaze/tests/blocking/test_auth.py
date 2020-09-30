import unittest

from .client import CLIENT

from ...models.auth import AuthModel


class TestBlockingAuth(unittest.TestCase):
    def test_auth(self):
        self.assertTrue(
            type(CLIENT.authorize()) == AuthModel
        )
