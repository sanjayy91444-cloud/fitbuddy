import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key, transport="rest")

def generate_nutrition_tip_with_flash(goal: str, weight: int) -> str:
    prompt = f"""
    You are an expert sports nutritionist.
    Provide a concise, practical nutrition and diet tip for someone with:
    - Current Weight: {weight} kg
    - Fitness Goal: {goal}

    Include:
    1. Daily hydration guideline (water intake).
    2. Recommended protein/carb balance.
    3. One practical dietary habit or food recommendation to achieve this goal faster.
    Keep the tone encouraging, crisp, and under 120 words.
    """

    model = genai.GenerativeModel("gemini-3.8-flash")
    response = model.generate_content(prompt)
    return response.text
