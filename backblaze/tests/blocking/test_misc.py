import unittest

from ...exceptions import AuthorizeRequired

from ... import Blocking as BlockingClient


class TestMiscBlocking(unittest.TestCase):
    def test_forgot_to_call_authorize(self):
        b2_client = BlockingClient("", "")

        with self.assertRaises(AuthorizeRequired):
            b2_client.download_by_name("", "")
