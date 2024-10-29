# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Allow CORS for your no-code website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your website’s domain in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserResponse(BaseModel):
    thinking_types: List[str]
    human_abilities: List[str]
    flow_activities: List[str]
    causes: List[str]
    problem_types: List[str]

class CareerSuggestion(BaseModel):
    titles: List[str]
    descriptions: List[str]

def generate_career_suggestions(user: UserResponse) -> CareerSuggestion:
    titles = []
    descriptions = []

    if "analytical" in user.problem_types:
        titles.append("Data Analyst")
        descriptions.append("Analyze data to help organizations make informed decisions.")

    if "social" in user.problem_types:
        titles.append("Human Resources Manager")
        descriptions.append("Manage employee relations and organizational culture.")

    if not titles:
        titles.append("Career Counselor")
        descriptions.append("Assist individuals in identifying career paths that suit their skills and interests.")

    return CareerSuggestion(titles=titles, descriptions=descriptions)

@app.post("/suggest-careers", response_model=CareerSuggestion)
def suggest_careers(user_response: UserResponse):
    try:
        return generate_career_suggestions(user_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
