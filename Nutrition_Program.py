import os
import requests
from dotenv import load_dotenv
import random
import time

# Load API keys from .env file
load_dotenv()
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")

# Part 1: Setting Goals
print("--- Part 1: Setting Fitness Goals ---")
name = input("Enter your name: ")
gender = input("Enter your gender (M/F): ")
height = float(input("Enter your height in cm: "))
current_weight = float(input("Enter your current weight in kg: "))
daily_calorie_intake = int(input("Enter your current daily calorie intake: "))
target_weight = float(input("Enter your target weight in kg: "))

# Ensure realistic goal timeline
while True:
    days_to_target = int(input("In how many days do you want to achieve your target? "))
    if abs(target_weight - current_weight) > 1 and days_to_target < 7:
        print("\nWarning: Attempting to change more than 1 kg in less than a week is not healthy. Please enter a more realistic timeline.")
    else:
        break

# Determine goal
goal = "gain weight" if target_weight > current_weight else "lose weight"
print(f"\nHello {name}, your goal is to {goal}.")

# Calculate required calorie adjustment (approx 7700 calories per kg)
calorie_difference = (abs(target_weight - current_weight) * 7700) / days_to_target

if goal == "gain weight":
    recommended_calories = daily_calorie_intake + calorie_difference
else:
    recommended_calories = daily_calorie_intake - calorie_difference

print(f"To {goal}, you should aim for {recommended_calories:.2f} calories per day.")

# Part 2: Dietary Recommendations
print("\n--- Part 2: Dietary Recommendations ---")
num_meals = int(input("How many meals would you like to have in a day to meet your goal? "))
meal_calories = recommended_calories / num_meals

print(f"\nHere is your meal plan:")

# Categorizing meals by calorie density
low_cal_meals = [
    "spinach salad with vinaigrette",
    "grilled zucchini with quinoa",
    "vegetable stir fry with tofu",
    "lentil soup with whole grain bread",
    "scrambled eggs with toast and spinach"
]

medium_cal_meals = [
    "grilled chicken breast with quinoa and avocado",
    "salmon with brown rice and vegetables",
    "shrimp stir fry with jasmine rice",
    "turkey sandwich with whole grain bread",
    "stuffed bell peppers with ground turkey"
]

high_cal_meals = [
    "beef steak with sweet potatoes",
    "pasta with tomato sauce and cheese",
    "falafel wrap with hummus and tabbouleh",
    "chickpea salad with olive oil and feta",
    "grilled pork chops with mashed potatoes",
    "cheeseburger with fries",
    "chicken alfredo pasta",
    "bacon and eggs with toast",
    "avocado toast with poached eggs",
    "banana smoothie with peanut butter",
    "loaded nachos with cheese and guacamole",
    "fried chicken with coleslaw",
    "pizza with pepperoni and extra cheese",
    "bbq ribs with baked beans",
    "pancakes with syrup and butter"
]

# Combine and shuffle all meals
all_meals = low_cal_meals + medium_cal_meals + high_cal_meals
random.shuffle(all_meals)

# Function to handle API retries
def fetch_meal_data(query, retries=3):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"query": query}

    for attempt in range(retries):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return None
    return None

# Function to suggest meals based on calorie need
def suggest_meal(target_calories, used_queries, tolerance=0.25):
    available_queries = list(set(all_meals) - set(used_queries))
    if not available_queries:
        return None, 0

    best_meal = None
    best_calories = 0
    attempts = min(5, len(available_queries))  # Try up to 5 different meals
    
    for _ in range(attempts):
        query = random.choice(available_queries)
        available_queries.remove(query)
        used_queries.append(query)
        food_data = fetch_meal_data(query)

        if food_data:
            meal_details = []
            total_calories = total_protein = total_fat = total_carbs = 0

            for item in food_data.get('foods', []):
                name = item['food_name']
                calories = item.get('nf_calories', 0)
                protein = item.get('nf_protein', 0)
                fat = item.get('nf_total_fat', 0)
                carbs = item.get('nf_total_carbohydrate', 0)

                total_calories += calories
                total_protein += protein
                total_fat += fat
                total_carbs += carbs

                meal_details.append(
                    f"{name.title()} - 1 serving(s), {calories:.0f} cal, {protein:.1f}g protein, {fat:.1f}g fat, {carbs:.1f}g carbs"
                )

            # Check if this meal is closer to our target than the previous best
            if best_meal is None or abs(target_calories - total_calories) < abs(target_calories - best_calories):
                best_meal = ('\n'.join(meal_details) + 
                            f"\nTotal: {total_calories:.0f} cal, {total_protein:.1f}g protein, {total_fat:.1f}g fat, {total_carbs:.1f}g carbs")
                best_calories = total_calories

    return (best_meal, best_calories) if best_meal else ("Unable to fetch meal suggestion at this time.", 0)

# Suggest meals with better distribution
used_queries = []
total_meal_calories = 0
remaining_calories = recommended_calories
remaining_meals = num_meals

for i in range(1, num_meals + 1):
    # Calculate target calories for this meal
    target_meal_calories = remaining_calories / remaining_meals
    
    # Try to get a meal close to the target
    suggested_meal, meal_cal = suggest_meal(target_meal_calories, used_queries)
    
    if suggested_meal is None:
        break
        
    print(f"\nMeal {i}: {suggested_meal}")
    total_meal_calories += meal_cal
    
    # Update remaining calories and meals
    remaining_calories = recommended_calories - total_meal_calories
    remaining_meals -= 1

# Final summary
print(f"\nTotal planned calorie intake: {total_meal_calories:.2f} calories")
if abs(total_meal_calories - recommended_calories) / recommended_calories > 0.10:
    print("\nNote: Meal plan deviates from calorie goal by more than 10%.")
    print(f"Target: {recommended_calories:.2f} calories")
    print(f"Actual: {total_meal_calories:.2f} calories")
else:
    print("\nYour meal plan closely matches your calorie goal!")

# Part 3: Tracking Calories
print("\n--- Part 3: Tracking Calorie Intake ---")

def track_meal(meal_number):
    total_meal_calories = 0
    
    while True:
        food_item = input(f"Enter food item for Meal {meal_number} (or 'done' if finished with this meal): ")
        if food_item.lower() == 'done':
            break
            
        # Get serving size
        servings = float(input("How many servings did you have? (e.g., 1, 0.5, 2): "))
        
        food_data = fetch_meal_data(food_item)
        
        if food_data:
            meal_calories = 0
            print("\nNutritional information:")
            
            for item in food_data.get('foods', []):
                name = item['food_name']
                serving_unit = item.get('serving_unit', 'serving')
                serving_qty = item.get('serving_qty', 1)
                calories = item.get('nf_calories', 0)
                adjusted_calories = calories * servings
                
                print(f"{name.title()}:")
                print(f"- Standard serving: {serving_qty} {serving_unit}")
                print(f"- Calories per serving: {calories:.0f}")
                print(f"- Your serving size: {servings} {serving_unit}")
                print(f"- Your calories: {adjusted_calories:.0f}")
                
                meal_calories += adjusted_calories
            
            total_meal_calories += meal_calories
            print(f"\nRunning total for Meal {meal_number}: {total_meal_calories:.0f} calories")
        else:
            print("Error retrieving food data.")
    
    return total_meal_calories

# Track meals
total_calories_consumed = 0
for i in range(1, num_meals + 1):
    print(f"\n=== Tracking Meal {i} ===")
    meal_calories = track_meal(i)
    total_calories_consumed += meal_calories
    print(f"Total calories for Meal {i}: {meal_calories:.0f}")

# Display total and compare with recommended
print(f"\nTotal calories consumed today: {total_calories_consumed:.2f}")
calorie_difference = total_calories_consumed - recommended_calories

if abs(calorie_difference) <= 500:
    print("You're within 500 calories of your goal. Great job! Keep it up!")
elif calorie_difference > 500:
    print(f"You have exceeded your target by {calorie_difference:.2f} calories. Stay mindful, but a treat once in a while is okay!")
elif calorie_difference < -500:
    print(f"You missed your target by {-calorie_difference:.2f} calories. Don't worry, you can balance it out tomorrow!")