from pydantic import BaseModel
from datetime import datetime


class FileGenerationResponse(BaseModel):
    filename: str
    filesize: int
    url_link: str

    class Config:
        anystr_strip_whitespace: True


class FileLinksResponse(BaseModel):
    id: int
    filename: str
    created: datetime
    url_link: str
    url_report: str

    class Config:
        anystr_strip_whitespace: True
