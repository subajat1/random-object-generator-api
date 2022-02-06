import os
from datetime import datetime
from app import db

FILENAME_SIZE = int(os.getenv('g_FILENAME_SIZE', 16))


class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(FILENAME_SIZE), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, filename: str):
        self.filename = filename

    def __repr__(self) -> str:
        return 'File>>> {self.username}'

    @property
    def serialize(self) -> dict:
        """Serialize File object into dict object"""
        return {
            'id': self.id,
            'filename': self.filename+'.txt',
            'created': self.created,
        }
