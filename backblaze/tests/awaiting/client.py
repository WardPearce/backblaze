from ... import Awaiting
from ..shared_vars import KEY, KEY_ID

CLIENT = Awaiting(
    key_id=KEY_ID,
    key=KEY,
    timeout=320
)
