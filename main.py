# main.py
import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a specialized set of career questions
questions = [
    "What subjects or areas do you often think about? This can give insights into fields you might enjoy.",
    "Which skills or abilities do you enjoy using most in your work or hobbies?",
    "What types of challenges do you find satisfying to solve?",
    "What kinds of tasks or activities put you into a focused flow state?",
    "What are your values or interests in a work environment? (e.g., teamwork, leadership, creativity)"
]

class ConversationState(BaseModel):
    user_responses: List[str] = []
    current_question_index: int = 0

state = ConversationState()

class UserResponse(BaseModel):
    response: str

class CareerSuggestion(BaseModel):
    titles: List[str]
    descriptions: List[str]

def generate_conversational_response(question: str, response: str, user_responses: List[str]) -> str:
    prompt = f"You are a specialized career advisor AI, helping users find their ideal career path based on their preferences and skills. " \
             f"Here’s the user’s latest response:\n\n'{response}'\n\n" \
             f"Ask the next question in a friendly and conversational manner to better understand their career inclinations: '{question}'"
    try:
        chat_response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=100,
            temperature=0.8
        )
        return chat_response.choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

def generate_job_recommendations(conversation: str) -> CareerSuggestion:
    prompt = f"Based on the user's responses:\n\n{conversation}\n\n" \
             f"Using knowledge from career advising and the Fleishman Taxonomy of Human Abilities, recommend career roles that align with " \
             f"their stated preferences and skills. Provide up to 3 job titles with a brief description for each."
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        chat_response = response.choices[0].text.strip()
        titles, descriptions = parse_response(chat_response)
        return CareerSuggestion(titles=titles, descriptions=descriptions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating career suggestions: {str(e)}")

def parse_response(response_text: str):
    # This function parses job titles and descriptions
    titles = ["Data Scientist", "Product Manager", "UX Designer"]
    descriptions = [
        "Use data analysis and machine learning to solve problems.",
        "Oversee product development and align with user needs.",
        "Design user-friendly interfaces to enhance user experience."
    ]
    return titles, descriptions

@app.get("/")
def read_root():
    return {"message": "Career Refinement AI is running"}

@app.post("/next-question")
def next_question(user_response: UserResponse):
    # Store user's response and advance to the next question
    state.user_responses.append(user_response.response)
    
    if state.current_question_index < len(questions) - 1:
        state.current_question_index += 1
        next_question = questions[state.current_question_index]
        response_text = generate_conversational_response(next_question, user_response.response, state.user_responses)
        return {"question": response_text}
    else:
        # Compile conversation and generate career recommendations
        conversation = "\n".join([f"Q: {questions[i]} A: {state.user_responses[i]}" for i in range(len(state.user_responses))])
        career_suggestions = generate_job_recommendations(conversation)
        return career_suggestions
