import uuid
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import init_db, get_db, User, WorkoutPlan
from app.schemas import UserCreate, FeedbackRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

# FastAPI app initialize panrom
app = FastAPI(
    title="FitBuddy AI",
    description="AI-powered Fitness and Nutrition Planner using Google Gemini"
)

# App start aagumbodhu database tables create aagum
@app.on_event("startup")
def startup_event():
    init_db()

# 1. Health check endpoint
@app.get("/")
def home():
    return {"message": "FitBuddy AI backend is running smoothly!"}

# 2. Workout Plan & Nutrition Tip Generate panra API
@app.post("/generate-plan/")
def create_plan(user_data: UserCreate, db: Session = Depends(get_db)):
    # Ovvoru user-kum unique ID create panrom
    generated_user_id = f"user_{uuid.uuid4().hex[:8]}"

    # Gemini model moolama workout plan generate panrom
    try:
        workout_plan_text = generate_workout_gemini(
            name=user_data.name,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini AI Workout Error: {str(e)}")

    # Gemini Flash model moolama nutrition tip generate panrom
    try:
        nutrition_tip_text = generate_nutrition_tip_with_flash(
            goal=user_data.goal,
            weight=user_data.weight
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini Flash Nutrition Error: {str(e)}")

    # Database-la user details save panrom
    new_user = User(
        user_id=generated_user_id,
        name=user_data.name,
        age=user_data.age,
        weight=user_data.weight,
        goal=user_data.goal,
        intensity=user_data.intensity
    )
    db.add(new_user)

    # Database-la workout plan & nutrition tip save panrom
    new_plan = WorkoutPlan(
        user_id=generated_user_id,
        original_plan=workout_plan_text,
        nutrition_tip=nutrition_tip_text
    )
    db.add(new_plan)
    db.commit()

    return {
        "status": "success",
        "user_id": generated_user_id,
        "name": user_data.name,
        "workout_plan": workout_plan_text,
        "nutrition_tip": nutrition_tip_text
    }

# 3. User feedback vachi plan update panra API
@app.post("/update-plan/")
def modify_plan(feedback_data: FeedbackRequest, db: Session = Depends(get_db)):
    plan_record = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == feedback_data.user_id).first()

    if not plan_record:
        raise HTTPException(status_code=404, detail="User workout plan not found!")

    # Gemini model feedback vachi plan-ah update pannum
    try:
        updated_plan_text = update_workout_plan(
            original_plan=plan_record.original_plan,
            feedback=feedback_data.feedback
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan Update Error: {str(e)}")

    # Database-la update pannitu save panrom
    plan_record.feedback = feedback_data.feedback
    plan_record.updated_plan = updated_plan_text
    db.commit()

    return {
        "status": "success",
        "user_id": feedback_data.user_id,
        "updated_plan": updated_plan_text
    }

# 4. Specific user-oda data & plans edukkura API
@app.get("/user/{user_id}/")
def get_user_details(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    return {
        "user": {
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity
        },
        "original_plan": plan.original_plan if plan else None,
        "nutrition_tip": plan.nutrition_tip if plan else None,
        "updated_plan": plan.updated_plan if plan else None,
        "feedback": plan.feedback if plan else None
    }
