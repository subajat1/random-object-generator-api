import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Define Config for Flask App"""
    default_db = 'sqlite:///random-object-files.db'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_DB_URI', default_db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_FOLDER = f'{os.getenv("APP_FOLDER")}/app/media'

    SWAGGER = { 'title': 'Random-object Generator API',
                'uiversion': 3}
