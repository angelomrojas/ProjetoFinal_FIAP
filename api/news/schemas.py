from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class NewsIn(BaseModel):
    page: str
    url: str
    issued: datetime
    modified: datetime
    title: str
    body: str
    caption: str
    theme: str



