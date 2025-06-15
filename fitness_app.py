import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv('workout_fitness_tracker_data.csv')

# Preprocessing
df['Calories_per_min'] = df['Calories Burned'] / df['Workout Duration (mins)']

X = df[['Age', 'Weight (kg)', 'Calories_per_min', 'Workout Duration (mins)']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=5, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Workout clusters
cluster_profiles = {
    0: {'name': 'Light Maintainers', 'intensity': 'Low', 'type': 'Yoga/Pilates'},
    1: {'name': 'Cardio Focus', 'intensity': 'Medium', 'type': 'Running/Cycling'},
    2: {'name': 'HIIT Enthusiasts', 'intensity': 'High', 'type': 'HIIT/Interval Training'},
    3: {'name': 'Strength Builders', 'intensity': 'Medium-High', 'type': 'Strength Training'},
    4: {'name': 'Balanced Fitness', 'intensity': 'Varied', 'type': 'Mixed Routine'}
}

def get_recommendation(age, weight, gender, goal='maintenance', available_time=30):
    height = df[df['Gender'] == gender]['Height (cm)'].median() / 100
    bmi = weight / (height ** 2)

    if bmi < 18.5:
        intensity = 'Low-Medium'
    elif 18.5 <= bmi < 25:
        intensity = 'Medium'
    elif 25 <= bmi < 30:
        intensity = 'Medium-High'
    else:
        intensity = 'High'

    filtered = df[
        (df['Age'].between(age - 5, age + 5)) &
        (df['Weight (kg)'].between(weight - 5, weight + 5)) &
        (df['Gender'] == gender)
    ]
    if len(filtered) == 0:
        filtered = df

    top_workouts = filtered.groupby('Workout Type')['Calories_per_min'].mean().sort_values(ascending=False)

    return {
        'daily': f"15-20 min {intensity} {top_workouts.index[0]}",
        'weekly': [
            f"3-4 sessions of {top_workouts.index[0]} ({available_time} min)",
            f"2 sessions of {top_workouts.index[1]} ({available_time} min)",
            "1 active recovery day (Yoga/Stretching)"
        ],
        'monthly': [
            f"Gradually increase {top_workouts.index[0]} duration by 10%",
            "Try 1-2 new workout types for variety",
            "Schedule 1-2 rest days per week"
        ],
        'bmi': round(bmi, 1),
        'intensity_level': intensity,
        'top_workouts': list(top_workouts.index[:3])
    }

# --------------------------
# STREAMLIT INTERFACE
# --------------------------

st.title("🏋️‍♂️ Fitness Recommendation App")

age = st.number_input("Enter your age", min_value=10, max_value=100, value=30)
weight = st.number_input("Enter your weight (kg)", min_value=30, max_value=200, value=70)
gender = st.selectbox("Select your gender", options=df['Gender'].unique())
goal = st.selectbox("Your fitness goal", ['maintenance', 'weight loss', 'muscle gain'])
available_time = st.slider("Available workout time per session (minutes)", 10, 120, 30)

if st.button("Get Recommendation"):
    result = get_recommendation(age, weight, gender, goal, available_time)

    st.subheader("📊 Your Recommendation:")
    st.write(f"**BMI**: {result['bmi']} ({result['intensity_level']} intensity)")
    
    st.markdown(f"**Daily Suggestion:** {result['daily']}")
    st.markdown("**Weekly Plan:**")
    for item in result['weekly']:
        st.write(f"- {item}")
    
    st.markdown("**Monthly Goals:**")
    for item in result['monthly']:
        st.write(f"- {item}")
    
    st.markdown(f"**Top Workout Types for You:** {', '.join(result['top_workouts'])}")
