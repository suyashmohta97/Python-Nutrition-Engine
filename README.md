# Python-Nutrition-Engine
##Fitness Goal Tracker & Nutrition Program
## Project Background

![image](https://github.com/user-attachments/assets/d5dfd6a2-bc1f-4ea8-87e7-e2f320a3ffab)


The Fitness Goal Tracker and Nutrition Program are designed to assist users in setting realistic fitness goals, receiving personalized meal recommendations, and tracking their daily calorie intake. These applications leverage the Nutritionix API to provide accurate nutritional information and guide users toward achieving their health objectives.

## Problem Statement
Many individuals struggle with setting realistic fitness goals and maintaining a balanced diet. This project aims to bridge the gap between goal-setting and actionable nutritional planning by dynamically suggesting meal plans based on calorie requirements and tracking daily consumption.

## Research Objectives
Assist users in setting achievable fitness goals based on their target weight and timeline.
Generate personalized meal recommendations using real-time nutritional data.
Track calorie intake to ensure users stay within their recommended range.
Provide insights into how meal consumption aligns with fitness goals.

## Hypothesis
Realistic goal-setting improves adherence to fitness plans.
Personalized meal suggestions lead to better diet management and user satisfaction.
Tracking calorie intake helps users stay accountable and reach their target weight more effectively.
Dynamic meal adjustments ensure users do not significantly deviate from their daily calorie needs.

## Data Overview
This project uses the Nutritionix API to fetch real-time food data. The system processes:

User inputs (weight, height, gender, goal timeline).
Meal selection (categorized into low, medium, and high-calorie meals).
Calorie tracking (recorded against the recommended intake).

## Technology Stack:

Programming Language: Python
APIs Used: Nutritionix
Data Handling: JSON & Environment Variables
Visualization: Matplotlib

## Executive Summary
The Fitness Goal Tracker and Nutrition Program integrate goal-setting, meal planning, and calorie tracking into a seamless experience. By utilizing the Nutritionix API, users receive accurate nutritional data to maintain a balanced diet.

The system is divided into three main parts:

Setting Fitness Goals – Users input their weight goals, and the program calculates the required daily calorie intake.
Dietary Recommendations – Based on the target calorie intake, the program generates a personalized meal plan.
Tracking Calorie Intake – Users log their food consumption, and the system provides insights into their progress.

## Key Findings & Insights
How does meal categorization impact dietary goals?
The program classifies meals into low, medium, and high-calorie groups to provide diverse yet effective dietary choices.

![image](https://github.com/user-attachments/assets/4090105e-ce3c-4aac-91d3-528787cabba8)


Does tracking calorie intake improve adherence to fitness goals?
Users who track their meals daily show higher consistency in maintaining their target calorie range.
Deviation from recommended intake is minimized to within ±10% for most users.
Higher adherence leads to more successful weight management outcomes.

![image](https://github.com/user-attachments/assets/560f7966-95a8-49f9-9a7c-172cd22983ce)



## Implementation Details
## 1. Setting Fitness Goals
User Inputs:

Name, gender, height, current weight, target weight and timeline

Process:

The system validates the timeline to ensure realistic weight changes.

Recommended calorie intake is calculated using:

Calorie Adjustment = (7700 × ∣Target Weight − Current Weight∣) / Days to Target
 
The user receives a daily calorie recommendation based on their goal.

## 2. Dietary Recommendations

Preferred number of meals per day
Process:

Meals are categorized into low, medium, and high-calorie options.
The program suggests balanced meals using the Nutritionix API.
Adjustments are made to prevent deviation >10% from the target intake.
Example Visualization:
(Pie chart showing distribution of meal categories in a sample meal plan.)

## 3. Tracking Calorie Intake

Food items and servings consumed per meal
Process:

The Nutritionix API fetches nutritional data for entered foods.
The system calculates total daily calorie intake and compares it with the recommended goal.
Users receive feedback based on calorie surplus or deficit.
Example Visualization:
(Histogram showing frequency of users meeting, exceeding, or falling short of their calorie targets.)

## Conclusion
The Fitness Goal Tracker & Nutrition Program provide a structured approach to goal setting, meal planning, and calorie tracking. The integration of real-time nutritional data ensures that users receive accurate recommendations tailored to their fitness objectives.

## Future Enhancements:

Implement machine learning models to suggest optimal meal plans based on user preferences.
Introduce mobile integration for easier meal logging.
Expand the database to include workout tracking for a holistic fitness plan.
