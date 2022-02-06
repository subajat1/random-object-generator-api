import os
from enum import Enum
from random import Random


TESTING_ENV = os.getenv("g_TESTING_ENV", 'False').lower() in ('true', '1', 't')
FILENAME_SIZE = int(os.getenv('g_FILENAME_SIZE', 16))
SIZE_LIMIT_MB = int(os.getenv('g_SIZE_LIMIT_MB', 2)) * 1024 * 1024
DEFAULT_RAND_OBJ_SIZE = int(os.getenv('g_DEFAULT_RAND_OBJ_SIZE', 16))


class RandObjectType(Enum):
    ALPHABET = 0
    REAL_NUMBER = 1
    INTEGER = 2
    ALPHANUMERIC = 3


def genRandObjectType(rand: Random) -> RandObjectType:
    return RandObjectType(rand.randint(0, len(RandObjectType)-1))


def genRandObjectSizeInRange(rand: Random, min: int, max: int) -> str:

    if TESTING_ENV or min <= 0 or max <= 0:
        return DEFAULT_RAND_OBJ_SIZE

    elif min >= max:
        return min

    else:
        return rand.randint(min, max)
