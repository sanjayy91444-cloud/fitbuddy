import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env file-la irukra API key-ah load panrom
load_dotenv()

# Gemini AI-kku secret key kuduthu connect panrom
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_workout_gemini(name: str, age: int, weight: int, goal: str, intensity: str) -> str:
    prompt = f"""
    You are an expert AI fitness coach. Create a personalized 7-day workout plan for:
    - Name: {name}
    - Age: {age}
    - Weight: {weight} kg
    - Fitness Goal: {goal}
    - Intensity Level: {intensity}

    Please provide:
    1. A short, motivating welcome note for {name}.
    2. Day 1 to Day 7 structured routine (Exercise names, sets, reps, and rest time).
    3. Warm-up and cool-down instructions.
    Keep the formatting clean, structured, and easy to read.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
