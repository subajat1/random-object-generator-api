
import os
from app.config import basedir


def parseRandObjectsFromFile(filename: str) -> dict:

    if not filename:
        return {}

    filepath = os.path.join(f'{basedir}/media', filename + '.txt')

    CNT_ALPHABET = 0
    CNT_REAL_NUM = 0
    CNT_INTEGER = 0
    CNT_ALPHANUMERIC = 0
    DELIMITER = ','
    DECIMAL_POINT = '.'
    file_stats = {}

    with open(filepath, 'r') as file:
        objects = file.read().split(DELIMITER)

        for obj in objects:

            if DECIMAL_POINT in obj:
                try:
                    if float(obj):
                        CNT_REAL_NUM += 1
                except ValueError:
                    print(f'ValueError parseToFloat: {obj}')

            elif obj.isnumeric():
                try:
                    if int(obj):
                        CNT_INTEGER += 1
                except ValueError:
                    print(f'ValueError parseToInt: {obj}')

            elif obj.isalpha():
                try:
                    if str(obj):
                        CNT_ALPHABET += 1
                except ValueError:
                    print(f'ValueError parseToInt: {obj}')

            elif obj.isalnum():
                try:
                    if str(obj):
                        CNT_ALPHANUMERIC += 1
                except ValueError:
                    print(f'ValueError parseToInt: {obj}')

    file_stats['count_alphabet'] = CNT_ALPHABET
    file_stats['count_real_num'] = CNT_REAL_NUM
    file_stats['count_integer'] = CNT_INTEGER
    file_stats['count_alphanumeric'] = CNT_ALPHANUMERIC

    return file_stats
