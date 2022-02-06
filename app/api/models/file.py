from datetime import datetime
from app import db


class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(16), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, filename: str):
        self.filename = filename

    def __repr__(self) -> str:
        return 'File>>> {self.username}'
