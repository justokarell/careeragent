# models.py
from pydantic import BaseModel
from typing import List

# Model for individual user responses to each question
class UserResponse(BaseModel):
    response: str  # Single response to each question

# Model to maintain conversation state and keep track of user responses and question index
class ConversationState(BaseModel):
    user_responses: List[str] = []  # Stores each response sequentially
    current_question_index: int = 0  # Tracks which question is currently being asked

# Model for career suggestions that the API will return
class CareerSuggestion(BaseModel):
    titles: List[str]  # Suggested job titles
    descriptions: List[str]  # Job descriptions for each suggested title
