import os
from random import Random

from flask import (
    Blueprint,
    Response,
    send_from_directory,
    request,
)
from flask_api import status
from flask_pydantic import validate

from app import db, app
from app.api.models.file import File

from app.api.schemas.file import (
    FileGenerationResponse,
    FileLinksResponse,
    FileReportResponse,)

from app.utils.generatorUtil import (
    genRandObjects,
    genAlphanumericRandObject,)

from app.utils.parserUtil import parseRandObjectsFromFile


RANDOM_SEED = str(os.getenv('g_RANDOM_SEED', 'random_seed'))
TESTING_ENV = os.getenv("g_TESTING_ENV", 'False').lower() in ('true', '1', 't')
FILENAME_SIZE = int(os.getenv('g_FILENAME_SIZE', 16))
MIN_SIZE = int(os.getenv('g_MIN_SIZE', 16))
MAX_SIZE = int(os.getenv('g_MAX_SIZE', 256))

bp = Blueprint('bp-rand-object', __name__)
route_path = 'api/rand-object'
url_prefix = f'/{route_path}'


@bp.route('/generate', methods=['GET'])
@validate(on_success_status=status.HTTP_201_CREATED)
def generate_random_objects() -> Response:
    """
    Generates random-objects put into the file with db-valid filename
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

        base_url = request.url_root + route_path
        url_link = base_url + '/link/' + filename

        db.session.add(File(filename=filename))
        db.session.commit()

    return FileGenerationResponse(
        filename=filename,
        filesize=filesize,
        url_link=url_link)


@bp.route('/link/<path:filename>')
@validate(on_success_status=status.HTTP_200_OK)
def retrieve_file(filename: str) -> Response:
    """
    Retrieves a file which file's name is from given filename path param value.
    Path param: filename (string) represent a file's name (without extension)
    Response: Response object (plain/text file)
    """

    try:
        return send_from_directory(
            app.config['MEDIA_FOLDER'],
            f'{filename}.txt')

    except Exception as e:
        return Response(
            f'File not found: {str(e)}',
            status=status.HTTP_404_NOT_FOUND)


@bp.route('/list/', methods=['GET'])
@validate(on_success_status=status.HTTP_200_OK, response_many=True)
def list_file() -> Response:

    files = File.query.all()

    if files:
        base_url = request.url_root + route_path

        responses = []
        for file in files:
            responses.append(
                FileLinksResponse(
                    id=file.id,
                    filename=file.filename+'.txt',
                    created=file.created,
                    url_link=base_url + '/link/' + file.filename,
                    url_report=base_url + '/report/' + file.filename,))

        return responses

    else:
        return Response('No file in db.', status=status.HTTP_204_NO_CONTENT)


@bp.route('/report/<path:filename>')
@validate(on_success_status=status.HTTP_200_OK)
def generate_report(filename: str) -> Response:

    files = File.query.filter(File.filename == filename).all()

    if files:
        stats = parseRandObjectsFromFile(files[0].filename)

        return FileReportResponse(
            stats=stats,
            file=files[0].serialize,)

    else:
        return Response('File not found', status=status.HTTP_404_NOT_FOUND)
