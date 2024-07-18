from enum import Enum
class MsgType(Enum):
    SYSTEM = 1
    USER = 2
    ASSISTANT = 3
    FUNCTION_CALL = 4
    FUNCTION_RESULT = 5
