import streamlit as st
import requests

# Page UI Configuration
st.set_page_config(
    page_title="FitBuddy AI - Smart Fitness Coach",
    page_icon="🏋️️‍♂️",
    layout="wide"
)

API_BASE_URL = "http://127.0.0.1:8000"

st.title("🏋️‍♂️ FitBuddy AI — Intelligent Fitness Assistant")
st.caption("Powered by FastAPI, SQLite & Google Gemini AI")

# Sidebar - User Inputs
with st.sidebar:
    st.header("👤 Your Profile Details")
    name = st.text_input("Name", value="Sanjay")
    age = st.number_input("Age", min_value=14, max_value=80, value=20)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=54)
    height = st.number_input("Height (cm)", min_value=100, max_value=230, value=170)
    
    goal = st.selectbox(
        "Fitness Goal",
        ["Muscle Building and Fitness", "Fat Loss & Lean Muscle", "Endurance & Stamina", "General Health"]
    )
    intensity = st.selectbox("Intensity Level", ["Beginner", "Intermediate", "Advanced"], index=1)

    # Real-time BMI Metric Calculation
    bmi = weight / ((height / 100) ** 2)
    st.divider()
    st.metric(label="Calculated BMI", value=f"{bmi:.1f}")
    if bmi < 18.5:
        st.info("Category: Lean / High Metabolism")
    elif 18.5 <= bmi < 24.9:
        st.success("Category: Ideal / Athletic Range")
    else:
        st.warning("Category: Overweight")

    generate_btn = st.button("🚀 Generate My AI Plan", use_container_width=True, type="primary")

# Main Dashboard Operations
if generate_btn:
    payload = {
        "name": name,
        "age": int(age),
        "weight": int(weight),
        "goal": goal,
        "intensity": intensity
    }
    
    with st.spinner("🤖 FitBuddy AI is analyzing your metrics and drafting your routine..."):
        try:
            response = requests.post(f"{API_BASE_URL}/generate-plan/", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.session_state["user_data"] = data
                st.success("Plan generated and saved to SQLite Database successfully!")
            else:
                st.error(f"Backend Error ({response.status_code}): {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("FastAPI Backend run aagala! Terminal-la: uvicorn app.main:app --reload run pannunga.")

# Display Generated Plan
if "user_data" in st.session_state:
    user_data = st.session_state["user_data"]
    
    tab1, tab2, tab3 = st.tabs(["📅 7-Day Workout Routine", "🥗 Nutrition & Diet Tip", "🔄 Adjust Plan (Feedback)"])
    
    with tab1:
        st.subheader("Your Personalized Workout Routine")
        st.markdown(user_data.get("workout_plan", "No plan available"))
    
    with tab2:
        st.subheader("Targeted Nutrition Guidance")
        st.info(user_data.get("nutrition_tip", "No tips available"))
    
    with tab3:
        st.subheader("Need Adjustments?")
        feedback = st.text_area(
            "Give feedback to AI (e.g., 'Focus more on core & biceps', 'Only 30 mins available on Day 3'):"
        )
        if st.button("Update Workout Plan"):
            if feedback.strip():
                with st.spinner("Refining plan with Gemini AI..."):
                    update_payload = {
                        "user_id": user_data.get("user_id"),
                        "feedback": feedback
                    }
                    try:
                        res = requests.post(f"{API_BASE_URL}/update-plan/", json=update_payload)
                        if res.status_code == 200:
                            updated_data = res.json()
                            st.session_state["user_data"]["workout_plan"] = updated_data.get("updated_plan")
                            st.success("Workout plan updated dynamically!")
                            st.rerun()
                        else:
                            st.error(f"Update failed: {res.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter your feedback before submitting.")
