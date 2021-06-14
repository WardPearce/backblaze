import unittest
import sys

from backblaze.tests.blocking.test_auth import *  # noqa: F403, F401
from backblaze.tests.blocking.test_bucket import *  # noqa: F403, F401
from backblaze.tests.blocking.test_key import *  # noqa: F403, F401
from backblaze.tests.blocking.test_files import *  # noqa: F403, F401
from backblaze.tests.blocking.test_file import *  # noqa: F403, F401
from backblaze.tests.blocking.test_misc import *  # noqa: F403, F401


from backblaze.tests.awaiting.test_auth import *  # noqa: F403, F401
from backblaze.tests.awaiting.test_bucket import *  # noqa: F403, F401
from backblaze.tests.awaiting.test_key import *  # noqa: F403, F401
from backblaze.tests.awaiting.test_files import *  # noqa: F403, F401
from backblaze.tests.awaiting.test_file import *  # noqa: F403, F401
from backblaze.tests.awaiting.test_misc import *  # noqa: F403, F401


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
