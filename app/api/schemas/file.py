from pydantic import BaseModel


class FileGenerationResponse(BaseModel):
    filename: str
    filesize: int

    class Config:
        anystr_strip_whitespace: True
