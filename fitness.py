{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "d82629cc-9743-4f93-93ba-796f4f822345",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'daily': '15-20 min Medium Cardio', 'weekly': ['3-4 sessions of Cardio (45 min)', '2 sessions of Yoga (45 min)', '1 active recovery day (Yoga/Stretching)'], 'monthly': ['Gradually increase Cardio duration by 10%', 'Try 1-2 new workout types for variety', 'Schedule 1-2 rest days per week'], 'bmi': np.float64(23.1), 'intensity_level': 'Medium', 'top_workouts': ['Cardio', 'Yoga', 'Strength']}\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from sklearn.cluster import KMeans\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "\n",
    "# Load and preprocess data (using your dataset)\n",
    "df = pd.read_csv('workout_fitness_tracker_data.csv')\n",
    "\n",
    "# Feature engineering\n",
    "df['Calories_per_min'] = df['Calories Burned'] / df['Workout Duration (mins)']\n",
    "\n",
    "# Create recommendation clusters\n",
    "X = df[['Age', 'Weight (kg)', 'Calories_per_min', 'Workout Duration (mins)']]\n",
    "scaler = StandardScaler()\n",
    "X_scaled = scaler.fit_transform(X)\n",
    "\n",
    "kmeans = KMeans(n_clusters=5, random_state=42)\n",
    "df['Cluster'] = kmeans.fit_predict(X_scaled)\n",
    "\n",
    "# Define cluster characteristics\n",
    "cluster_profiles = {\n",
    "    0: {'name': 'Light Maintainers', 'intensity': 'Low', 'type': 'Yoga/Pilates'},\n",
    "    1: {'name': 'Cardio Focus', 'intensity': 'Medium', 'type': 'Running/Cycling'},\n",
    "    2: {'name': 'HIIT Enthusiasts', 'intensity': 'High', 'type': 'HIIT/Interval Training'},\n",
    "    3: {'name': 'Strength Builders', 'intensity': 'Medium-High', 'type': 'Strength Training'},\n",
    "    4: {'name': 'Balanced Fitness', 'intensity': 'Varied', 'type': 'Mixed Routine'}\n",
    "}\n",
    "\n",
    "def get_recommendation(age, weight, gender, goal='maintenance', available_time=30):\n",
    "    \"\"\"Generate personalized workout recommendations\"\"\"\n",
    "    \n",
    "    # Calculate BMI\n",
    "    height = df[df['Gender'] == gender]['Height (cm)'].median() / 100  # Average height for gender\n",
    "    bmi = weight / (height ** 2)\n",
    "    \n",
    "    # Determine intensity level\n",
    "    if bmi < 18.5:\n",
    "        intensity = 'Low-Medium'\n",
    "    elif 18.5 <= bmi < 25:\n",
    "        intensity = 'Medium'\n",
    "    elif 25 <= bmi < 30:\n",
    "        intensity = 'Medium-High'\n",
    "    else:\n",
    "        intensity = 'High'\n",
    "    \n",
    "    # Filter workouts based on parameters\n",
    "    filtered = df[\n",
    "        (df['Age'].between(age-5, age+5)) &\n",
    "        (df['Weight (kg)'].between(weight-5, weight+5)) &\n",
    "        (df['Gender'] == gender)\n",
    "    ]\n",
    "    \n",
    "    if len(filtered) == 0:\n",
    "        filtered = df  # Fallback to all data if no matches\n",
    "    \n",
    "    # Get most effective workouts for similar profiles\n",
    "    top_workouts = filtered.groupby('Workout Type')['Calories_per_min'].mean().sort_values(ascending=False)\n",
    "    \n",
    "    # Generate recommendations\n",
    "    recommendations = {\n",
    "        'daily': f\"15-20 min {intensity} {top_workouts.index[0]}\",\n",
    "        'weekly': [\n",
    "            f\"3-4 sessions of {top_workouts.index[0]} ({available_time} min)\",\n",
    "            f\"2 sessions of {top_workouts.index[1]} ({available_time} min)\",\n",
    "            \"1 active recovery day (Yoga/Stretching)\"\n",
    "        ],\n",
    "        'monthly': [\n",
    "            f\"Gradually increase {top_workouts.index[0]} duration by 10%\",\n",
    "            \"Try 1-2 new workout types for variety\",\n",
    "            \"Schedule 1-2 rest days per week\"\n",
    "        ],\n",
    "        'bmi': round(bmi, 1),\n",
    "        'intensity_level': intensity,\n",
    "        'top_workouts': list(top_workouts.index[:3])\n",
    "    }\n",
    "    \n",
    "    return recommendations\n",
    "\n",
    "## Example Usage\n",
    "print(get_recommendation(age=30, weight=70, gender='Male', goal='weight loss', available_time=45))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "fc99e061-e288-4982-b45d-639f35e959cf",
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'model' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[1], line 4\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mjoblib\u001b[39;00m\n\u001b[0;32m      3\u001b[0m \u001b[38;5;66;03m# Suppose your trained model is stored in a variable called 'model'\u001b[39;00m\n\u001b[1;32m----> 4\u001b[0m joblib\u001b[38;5;241m.\u001b[39mdump(\u001b[43mmodel\u001b[49m, \u001b[38;5;124m'\u001b[39m\u001b[38;5;124mfitness_model.pkl\u001b[39m\u001b[38;5;124m'\u001b[39m)  \u001b[38;5;66;03m# saves the model to a file\u001b[39;00m\n",
      "\u001b[1;31mNameError\u001b[0m: name 'model' is not defined"
     ]
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "31ecc5a1-1ddf-4325-9105-442a169868fd",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
