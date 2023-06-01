from pydantic import BaseModel

class News(BaseModel):
    news_content: str
    feedback_content_type: str
    feedback_event_category: str