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


class FileResponse(BaseModel):
    id: int
    filename: str
    created: datetime

    class Config:
        anystr_strip_whitespace: True


class FileStatResponse(BaseModel):
    count_alphabet: int
    count_real_num: int
    count_integer: int
    count_alphanumeric: int


class FileReportResponse(BaseModel):
    stats: FileStatResponse
    file: FileResponse
