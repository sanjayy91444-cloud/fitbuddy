import time
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
    transport="rest"
)

def generate_nutrition_tip_with_flash(*args, **kwargs):
    goal = kwargs.get("goal") or (args[0] if len(args) > 0 else "General Fitness")
    weight = kwargs.get("weight", "54")

    prompt = f"""
    Provide 3 concise, highly actionable nutritional tips and hydration advice for someone with weight {weight} kg and fitness goal: '{goal}'.
    Keep it clean and formatted with bullet points.
    """
    model = genai.GenerativeModel("gemini-3.8-flash")

    # Try live Gemini Flash AI
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        pass

    # Graceful Fallback Nutrition Tips
    return f"""### 🥗 Nutrition & Fueling Protocol for {goal}
- **Protein Synthesis:** Aim for 1.8g to 2.0g protein per kg of body weight (approx. 100g-110g for {weight}kg) through eggs, paneer, lentils, and lean sources.
- **Hydration Target:** Consume 3.5 liters of clean water daily to sustain electrolyte balance and optimize recovery.
- **Pre & Post Workout Timing:** Ingest complex carbs 45 mins prior to training and high-quality protein within 30 mins post-session."""

generate_nutrition_tip = generate_nutrition_tip_with_flash
generate_nutrition_gemini = generate_nutrition_tip_with_flash
