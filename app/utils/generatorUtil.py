import os
import string
import math
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


def genAlphabetRandObject(rand: Random, size: int) -> str:
    return ''.join(rand.choices(string.ascii_letters, k=size))


def genIntegerRandObject(rand: Random, size: int) -> int:
    return int(''.join(rand.choices(string.digits, k=size)))


def genRealNumberRandObject(rand: Random, size: int) -> float:
    num = ''.join(rand.choices(string.digits, k=math.floor(0.40*size)))
    dec = ''.join(rand.choices(string.digits, k=math.floor(0.60*size)))
    return float(num + '.' + dec)


def genAlphanumericRandObject(rand: Random, size: int) -> str:
    return ''.join(rand.choices(string.digits + string.ascii_letters, k=size))


def genRandomObject(rand: Random, sizeMin: int, sizeMax: int) -> object:

    objectType = genRandObjectType(rand)
    objectSize = genRandObjectSizeInRange(rand, sizeMin, sizeMax)

    try:
        if objectType == RandObjectType.ALPHABET:
            return genAlphabetRandObject(rand, objectSize)
        elif objectType == RandObjectType.REAL_NUMBER:
            return genRealNumberRandObject(rand, objectSize)
        elif objectType == RandObjectType.INTEGER:
            return genIntegerRandObject(rand, objectSize)
        elif objectType == RandObjectType.ALPHANUMERIC:
            return genAlphanumericRandObject(rand, objectSize)
    except ValueError:
        print('ValueError during genRandomObject')
    except Exception as e:
        print(f'Exception {e.__class__} in genRandomObject')
