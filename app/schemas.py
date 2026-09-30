from pydantic import BaseModel
from typing import Optional

# User workout plan request panra input data format
class UserCreate(BaseModel):
    name: str
    age: int
    weight: int
    goal: str
    intensity: str

# User feedback kuduthu plan update panra format
class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str
