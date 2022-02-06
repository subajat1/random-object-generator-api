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

from sqlalchemy.exc import IntegrityError

from app import db, app
from app.api.models.file import File

from app.api.schemas.file import (
    FileGenerationResponse,
    FileLinksResponse,
    FileReportResponse,)

from app.utils.generatorUtil import (
    genRandObjects,
    genValidFilename,)

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

    filename = genValidFilename(rand, FILENAME_SIZE, 3)

    if filename:
        filesize = genRandObjects(rand, filename, MIN_SIZE, MAX_SIZE)
        url_link = request.url_root + route_path + '/link/' + filename

        try:
            db.session.add(File(filename=filename))
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        except Exception as e:
            # TODO: refactor to logging
            print(f'Exception {e.__class__} in generate_random_objects \
                when inserting File {filename} to db')

        return FileGenerationResponse(
            filename=filename,
            filesize=filesize,
            url_link=url_link)

    else:
        return Response(
                'Generation failed, filename exists.',
                status=status.HTTP_400_BAD_REQUEST)


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
    """
    Generates a report from a file about the total number of each random
    object types.
    """
    file = File.query.filter(File.filename == filename).first()

    if file:
        stats = parseRandObjectsFromFile(file.filename)

        return FileReportResponse(
            stats=stats,
            file=file.serialize,)

    else:
        return Response('File not found', status=status.HTTP_404_NOT_FOUND)
