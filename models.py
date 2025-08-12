from pydantic import BaseModel, field_validator
from typing import List, Union

class EmailData(BaseModel):
    from_: str
    to: Union[str, List[str]]
    cc: Union[str, List[str]]
    subject: str
    body: str

    @field_validator('to', 'cc', mode='before')
    def split_emails(cls, value):
        if isinstance(value, list):
            return value
        elif isinstance(value, str):
            return [email.strip() for email in value.split(',') if email.strip()]
        else:
            return []

class EmailText(BaseModel):
    body: str
