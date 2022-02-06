from pydantic import BaseModel


class FileGenerationResponse(BaseModel):
    filename: str
    filesize: int
    url_link: str

    class Config:
        anystr_strip_whitespace: True
