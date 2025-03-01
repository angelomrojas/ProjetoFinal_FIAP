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
    
class NewsGetIn(BaseModel):
    theme:str
    
class InteractionsIn(BaseModel):
    userId: str
    history: str
    scrollPercentageHistory: float
    pageVisitsCountHistory: int
    timeOnPageHistory: str
    
class UsersIn(BaseModel):
    id: str
    
class InterecationsList(BaseModel):
    Interecation: list[InteractionsIn]
    
    



