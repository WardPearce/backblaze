from ... import Blocking
from ..shared_vars import KEY, KEY_ID

CLIENT = Blocking(
    key_id=KEY_ID,
    key=KEY,
    timeout=320
)
