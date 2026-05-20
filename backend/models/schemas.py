from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MeetingOverview(BaseModel):
    主題: Optional[str] = None
    日期: Optional[str] = None
    與會人員: Optional[List[str]] = []
    重點摘要: Optional[str] = None

class ActionItem(BaseModel):
    項目名稱: str
    負責人: Optional[str] = None
    狀態: str = "pending"
    截止日期: Optional[str] = None

class AnalyzeRequest(BaseModel):
    text: str
    source: str = "text_input"

class AnalyzeResponse(BaseModel):
    success: bool
    data: dict
    excel_filename: Optional[str] = None
    created_at: Optional[datetime] = None

class HistoryRecord(BaseModel):
    id: str
    created_at: datetime
    meeting_topic: str
    excel_filename: str