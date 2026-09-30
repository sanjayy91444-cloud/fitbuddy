import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key, transport="rest")

def update_workout_plan(original_plan: str, feedback: str) -> str:
    prompt = f"""
    You are an expert AI fitness coach.
    A user has reviewed their 7-day workout plan and provided feedback.

    Original Workout Plan:
    {original_plan}

    User Feedback / Constraints:
    {feedback}

    Task:
    Update and adjust the 7-day workout plan strictly addressing the user's feedback.
    - Modify the exercises, reps, or intensity as requested.
    - Retain the clean day-by-day structure (Day 1 to Day 7).
    - Add a short introductory note explaining what adjustments were made.
    """

    model = genai.GenerativeModel("gemini-3.8-flash")
    response = model.generate_content(prompt)
    return response.text
