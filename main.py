# main.py
import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models import UserResponse, CareerSuggestion  # Import models
from typing import List
import os

app = FastAPI()

# Replace with your OpenAI API key
openai.api_key = os.getenv("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")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your website’s domain in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize prompt templates for questions
questions = [
    "What types of things do you find yourself thinking about often, for no particular reason? (For example, 'I think about how I could have handled social situations better.' or 'I think about the economy and interest labor metrics.')",
    "What types of skills or human abilities do you enjoy using? (e.g., Coding, creating food or art, writing, managerial communication, management, etc.)",
    "What types of problems do you enjoy solving?",
    "What types of activities get you into a flow state? (e.g., solving math problems, coding, writing, making new logos, biking, talking, moving heavy things, organizing, etc.)"
]

class ConversationState(BaseModel):
    user_responses: List[str] = []

state = ConversationState()

def generate_response(prompt: str) -> str:
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # Replace with the model you're using
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't generate a response."

@app.post("/next-question")
def next_question(user_response: UserResponse):
    # Store user response for the current question
    state.user_responses.append(user_response.response)
    
    if len(state.user_responses) < len(questions):
        # Return the next question
        question = questions[len(state.user_responses)]
        return {"question": question}
    else:
        # All questions answered, proceed to suggest careers
        return {"message": "You've completed the questions!"}

@app.post("/suggest-careers", response_model=CareerSuggestion)
def suggest_careers():
    try:
        # Prepare the input for the ChatGPT prompt based on user responses
        user_input = "\n".join([f"Q: {questions[i]} A: {state.user_responses[i]}" for i in range(len(state.user_responses))])
        prompt = f"Based on the following responses:\n\n{user_input}\n\nUsing an updated Fleishman’s Taxonomy of Human Abilities and relevant job titles, suggest suitable career roles that align with the user's skills, interests, and flow activities."
        
        # Call ChatGPT to get career suggestions
        chat_response = generate_response(prompt)
        titles, descriptions = process_chat_response(chat_response)  # Parses response into titles and descriptions
        
        # Return the career suggestions
        return CareerSuggestion(titles=titles, descriptions=descriptions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def process_chat_response(response: str):
    # This is a placeholder for parsing ChatGPT response into job titles and descriptions
    # Here you would add logic to split the response into meaningful titles and descriptions
    titles = ["Data Analyst", "Project Manager"]  # Replace with parsed titles
    descriptions = ["Analyze data...", "Oversee projects..."]  # Replace with parsed descriptions
    return titles, descriptions
