import os
import string
import math
from enum import Enum
from random import Random
from app.config import basedir
from app.api.models.file import File

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
    """Generate a random-object type from RandObjectType values"""
    return RandObjectType(rand.randint(0, len(RandObjectType)-1))


def genRandObjectSizeInRange(rand: Random, min: int, max: int) -> int:
    """Generate an integer within range of given min and max values"""
    if TESTING_ENV or min <= 0 or max <= 0:
        return DEFAULT_RAND_OBJ_SIZE

    elif min >= max:
        return min

    else:
        return rand.randint(min, max)


def genAlphabetRandObject(rand: Random, size: int) -> str:
    """Generate an alphabet object in length of given size value"""
    obj_alpha = None

    try:
        obj_alpha = ''.join(rand.choices(string.ascii_letters, k=size))
    except ValueError:
        # TODO: refactor to logging
        print(f'ValueError during genAlphabetRandObject: {str(obj_alpha)}')
    except Exception as e:
        # TODO: refactor to logging
        print(f'Exception {e.__class__} in \
            genAlphabetRandObject: {str(obj_alpha)}')
    finally:
        return obj_alpha


def genIntegerRandObject(rand: Random, size: int) -> str:
    """Generate an integer object with digit(s) as in given size value"""
    obj_int = None
    obj = ''.join(rand.choices(string.digits, k=size))

    try:
        obj_int = int(obj)
        if obj_int:
            return obj
        else:
            return None
    except ValueError:
        # TODO: refactor to logging
        print(f'ValueError during genIntegerRandObject: {str(obj)}')
    except Exception as e:
        # TODO: refactor to logging
        print(f'Exception {e.__class__} in genIntegerRandObject: {str(obj)}')


def genRealNumberRandObject(rand: Random, size: int) -> str:
    """Generate a real-number object with digit(s) before period mark is
        in length of 40% of given size value, and digit(s) after
        period mark is in length of 60% of given size value.
    """
    obj_float = None
    num = ''.join(rand.choices(string.digits, k=math.floor(0.40*size)))
    dec = ''.join(rand.choices(string.digits, k=math.floor(0.60*size)))
    obj = num + '.' + dec

    try:
        obj_float = float(obj)
        if obj_float:
            return obj
        else:
            return None
    except ValueError:
        # TODO: refactor to logging
        print(f'ValueError during genRealNumberRandObject: {str(obj)}')
    except Exception as e:
        # TODO: refactor to logging
        print(f'Exception {e.__class__} in \
            genRealNumberRandObject: {str(obj)}')


def genAlphanumericRandObject(rand: Random, size: int) -> str:
    """Generate an alphanumeric object in length of given size value"""
    obj_alphanum = None

    try:
        obj_alphanum = ''.join(rand.choices(
            string.digits + string.ascii_letters,
            k=size))
    except ValueError:
        # TODO: refactor to logging
        print(f'ValueError during genAlphabetRandObject: {str(obj_alphanum)}')
    except Exception as e:
        # TODO: refactor to logging
        print(f'Exception {e.__class__} in \
            genAlphabetRandObject: {str(obj_alphanum)}')
    finally:
        return obj_alphanum


def genRandomObject(rand: Random, sizeMin: int, sizeMax: int) -> object:
    """Generate a random-object for a specific type from given randomizer,
        and randomized size from given sizeMin and sizeMax.
        It returns either single Alphabet, Real number, Integer, or
        Alphanumeric object.
    """

    objectType = genRandObjectType(rand)
    objectSize = genRandObjectSizeInRange(rand, sizeMin, sizeMax)

    if objectType == RandObjectType.ALPHABET:
        return genAlphabetRandObject(rand, objectSize)
    elif objectType == RandObjectType.REAL_NUMBER:
        return genRealNumberRandObject(rand, objectSize)
    elif objectType == RandObjectType.INTEGER:
        return genIntegerRandObject(rand, objectSize)
    elif objectType == RandObjectType.ALPHANUMERIC:
        return genAlphanumericRandObject(rand, objectSize)


def genRandObjects(rand: Random, filename: str, min: int, max: int) -> int:
    """Generate random-objects as much as SIZE_LIMIT_MB.
        Given filename must not exist in db, given randomizer works
        within range min and max values.
        It returns filesize (byte) of a generated file contains
        the random-objects.
    """

    filepath = os.path.join(f'{basedir}/media', f'{filename}.txt')
    filesize = 0

    with open(filepath, 'w') as file:

        while file.tell() < SIZE_LIMIT_MB:
            object = genRandomObject(rand, min, max)
            if object:
                file.write(f'{object},')

        filesize = file.tell()

    return filesize


def genValidFilename(rand: Random, filename_size: int,
                     retry_limit: int) -> str:
    """Generate filename with db-checking"""
    filename = ''
    retry = 0

    while retry < retry_limit:
        filename = genAlphanumericRandObject(rand, filename_size)
        retry += 1
        file = File.query.filter(File.filename == filename).first()
        if not file:
            break
        elif file and retry >= retry_limit:
            return None

    return filename
