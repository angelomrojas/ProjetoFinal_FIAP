from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class NewsIn(BaseModel):
    id: int
    page: str
    url: str
    issued: datetime
    modified: datetime
    title: str
    body: str
    caption: str
    
class InteractionsIn(BaseModel):
    userId: str
    history: str
    scrollPercentageHistory: float
    pageVisitsCountHistory: int
    timeOnPageHistory: str
    
class UsersIn(BaseModel):
    id: int
    id_default: str
    
class InterecationsList(BaseModel):
    Interecation: list[InteractionsIn]
    
    
class Recommend(BaseModel):
    user_id: list[str]
    news_id: list[str]
    
    



