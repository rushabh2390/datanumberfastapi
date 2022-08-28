from pydantic import BaseModel, ValidationError, validator


class MonthsIn(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    month: int

    @validator('month')
    def Month_between_1_to_12(cls, value):
        if value < 1 or value > 12:
            raise ValueError('month should be betwwen 1 to 12')
        return value


class Months(MonthsIn):
    """_summary_

    Args:
        MonthsIn (_type_): _description_
    """
    id: int
    day_checked: int

    class Config:
        orm_mode = True


class DatesIn(MonthsIn):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    day: int

    @validator('day')
    def date_between_1_to_31(cls, value):
        if value < 1 or value > 31:
            raise ValueError('day should be betwwen 1 to 31')
        return value


class DatesResponse(DatesIn):
    """_summary_

    Args:
        DatesIn (_type_): _description_
    """
    fact: str


class Dates(DatesResponse):
    """_summary_

    Args:
        DatesIn (_type_): Superclass have month and day

    Raises:
        ValueError: month should be between 1 to 12
        ValueError: _description_

    Returns:
        _type_: Dates Data have month date id and fact
    """
    id: int

    class Config:
        orm_mode = True
