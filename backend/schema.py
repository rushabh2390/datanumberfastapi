from tomlkit import string
from pydantic import BaseModel, ValidationError, validator


class Dates(BaseModel):
    id: int
    month: int
    day: int
    fact: str
    day_checked = str

    @validator('month')
    def Month_between_1_to_12(cls, value):
        if value < 1 or value > 12:
            raise ValueError('month should be betwwen 1 to 12')
        return value

    @validator('day')
    def date_between_1_to_31(cls, value):
        if value < 1 or value > 31:
            raise ValueError('day should be betwwen 1 to 31')
        return value

    class Config:
        orm_mode = True


class DatesResponse(BaseModel):
    month: int
    day: int
    fact: str
