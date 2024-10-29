# models.py
from pydantic import BaseModel
from typing import List

# Model for individual user responses to each question
class UserResponse(BaseModel):
    response: str  # Single response to each question

# Model for conversation state to keep track of user responses
class ConversationState(BaseModel):
    user_responses: List[str] = []  # Stores each response sequentially

# Model for the career suggestions that the API will return
class CareerSuggestion(BaseModel):
    titles: List[str]  # Job titles suggested
    descriptions: List[str]  # Descriptions for each suggested job

# # Model for the user's input data
# class UserResponse(BaseModel):
#     thinking_types: List[str]
#     human_abilities: List[str]
#     flow_activities: List[str]
#     causes: List[str]
#     problem_types: List[str]

# # Model for the career suggestions that the API will return
# class CareerSuggestion(BaseModel):
#     titles: List[str]
#     descriptions: List[str]
