import os
from random import Random

from flask import (
    Blueprint,
    Response,
)
from flask_api import status
from flask_pydantic import validate

from app import db
from app.api.models.file import File
from app.api.schemas.file import FileGenerationResponse
from app.utils.generatorUtil import (
    genRandObjects,
    genAlphanumericRandObject,)


RANDOM_SEED = str(os.getenv('g_RANDOM_SEED', 'random_seed'))
TESTING_ENV = os.getenv("g_TESTING_ENV", 'False').lower() in ('true', '1', 't')
FILENAME_SIZE = int(os.getenv('g_FILENAME_SIZE', 16))
MIN_SIZE = int(os.getenv('g_MIN_SIZE', 16))
MAX_SIZE = int(os.getenv('g_MAX_SIZE', 256))

bp = Blueprint('bp-rand-object', __name__)
url_prefix = '/api/rand-object'


@bp.route('/generate', methods=['GET'])
@validate(on_success_status=status.HTTP_201_CREATED)
def generate_random_objects() -> Response:
    """
    Generates random-objects put into the file with db-valid filename
    Request: -
    Response: FileGenerationResponse
    """
    rand = Random(RANDOM_SEED) if TESTING_ENV else Random()

    filename = ''
    retry = 0
    retry_threshold = 3

    while retry < retry_threshold:
        filename = genAlphanumericRandObject(rand, FILENAME_SIZE)
        retry += 1
        files = File.query.filter(File.filename == filename).all()
        if not files:
            break
        elif files and retry >= retry_threshold:
            return Response(
                'Generation failed, filename exists.',
                status=status.HTTP_400_BAD_REQUEST)

    if filename and retry < retry_threshold:
        filesize = genRandObjects(rand, filename, MIN_SIZE, MAX_SIZE)

        db.session.add(File(filename=filename))
        db.session.commit()

    return FileGenerationResponse(
        filename=filename,
        filesize=filesize,)
