from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class CurrencyExch(BaseModel):
    value_to: str
    value_from: str
    amount: float

    @field_validator('value_to')
    def value_1_validate(cls, val: str):
        if len(val) == 3:
            return val
        else:
            raise HTTPException(
                status_code=400,
                detail='The value must be 3 characters'
            )

    @field_validator('value_from')
    def value_2_validate(cls, val: str):
        if len(val) == 3:
            return val
        else:
            raise HTTPException(
                status_code=400,
                detail='The value must be 3 characters'
            )