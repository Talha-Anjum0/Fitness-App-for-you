This Python project provides personalized fitness recommendations based on user attributes like age, weight, gender, and available workout time. It uses clustering (KMeans) and statistical analysis to generate weekly workout plans suited to the user's profile.

🚀 Features
Reads and preprocesses data from a fitness dataset (workout_fitness_tracker_data.csv)

Computes Calories_per_min as a derived metric

Applies KMeans clustering to group users into fitness profiles

Provides personalized daily, weekly, and monthly workout plans

Calculates BMI and suggests an appropriate intensity level

Lists top 3 effective workout types for the user

Handles missing or unmatched profiles by falling back on general data# Fitness-App-for-you

🧠 How It Works
Load Dataset
The script loads a .csv file containing workout history and metrics.

Feature Engineering
Adds a new column: Calories_per_min = Calories Burned / Workout Duration.

Clustering
Scales relevant features and applies KMeans to segment users into fitness profiles.

Recommendation Function
Accepts user input (age, weight, gender, goal, available_time) and:

Calculates BMI

Assigns an intensity level

Suggests top workouts

Outputs personalized plan

