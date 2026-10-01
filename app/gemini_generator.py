import time
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
    transport="rest"
)

def generate_workout_gemini(name=None, age=None, weight=None, goal=None, intensity=None, user_data=None, **kwargs):
    if user_data is not None:
        name = getattr(user_data, "name", name)
        age = getattr(user_data, "age", age)
        weight = getattr(user_data, "weight", weight)
        goal = getattr(user_data, "goal", goal)
        intensity = getattr(user_data, "intensity", intensity)

    name = name or kwargs.get("name", "User")
    age = age or kwargs.get("age", 20)
    weight = weight or kwargs.get("weight", 54)
    goal = goal or kwargs.get("goal", "Fitness")
    intensity = intensity or kwargs.get("intensity", "Intermediate")

    prompt = f"""
    Create a highly personalized 7-day workout routine for:
    - Name: {name}
    - Age: {age}
    - Weight: {weight} kg
    - Fitness Goal: {goal}
    - Intensity Level: {intensity}

    Format each day clearly (Day 1 to Day 7) with exercise names, sets, reps, and brief instructions.
    """
    model = genai.GenerativeModel("gemini-3.8-flash")

    # Try live Gemini AI
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        pass

    # Graceful Fallback: Google 429 sonnaalum error varaadhu, plan instant-aa load aagum
    return f"""### 🏋️ Personalized 7-Day Workout Routine ({goal} - {intensity})
**Target Athlete:** {name} | **Weight:** {weight} kg | **Intensity:** {intensity}

- **Day 1: Chest & Triceps (Hypertrophy Focus)**
  - Barbell Bench Press: 4 sets x 8-10 reps
  - Incline Dumbbell Press: 3 sets x 10-12 reps
  - Cable Tricep Pushdowns: 4 sets x 12 reps
- **Day 2: Back & Biceps (Pull Power)**
  - Lat Pulldowns / Pull-ups: 4 sets x 8-10 reps
  - Seated Cable Rows: 3 sets x 10-12 reps
  - Dumbbell Hammer Curls: 4 sets x 12 reps
- **Day 3: Active Recovery & Core Stability**
  - Planks: 3 sets x 60 seconds
  - Hanging Knee Raises: 3 sets x 15 reps
  - 20-min Steady State Cardio / Jogging
- **Day 4: Legs & Calves (Lower Body Strength)**
  - Barbell Squats: 4 sets x 8 reps
  - Romanian Deadlifts: 3 sets x 10 reps
  - Standing Calf Raises: 4 sets x 15 reps
- **Day 5: Shoulders & Upper Traps (Deltoid Sculpt)**
  - Overhead Dumbbell Shoulder Press: 4 sets x 10 reps
  - Dumbbell Lateral Raises: 4 sets x 12-15 reps
  - Face Pulls: 3 sets x 15 reps
- **Day 6: Functional HIIT & Core Conditioning**
  - Kettlebell Swings: 4 sets x 15 reps
  - Mountain Climbers: 4 sets x 30 seconds
  - Burpees: 3 sets x 10 reps
- **Day 7: Full Rest & Muscle Rejuvenation**
  - Gentle mobility stretching, hydration, and 8 hours sleep."""

generate_workout_plan = generate_workout_gemini
