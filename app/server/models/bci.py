from typing import Optional

from pydantic import BaseModel, Field


class BciSchema(BaseModel):
    pid: str = Field(...)
    emo: str = Field(...)
    time: str = Field(...)


    class Config:
        schema_extra = {
            "example": {
                "pid": "0",
                "emo": "null",
                "time":"null"
            }
        }


class UpdateBciModel(BaseModel):
    pid: Optional[str]
    emo: Optional[str]
    time:Optional[str]


    class Config:
        schema_extra = {
            "example": {
                "pid": "null",
                "emo": "null",
                "time": "null",

            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
