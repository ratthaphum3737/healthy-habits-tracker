import requests
from deep_translator import GoogleTranslator

APP_ID = "7bef5933"
API_KEY = "27d2b80ca482b5e2b975ab873cdc86ed"
HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json"
}

def translate_to_english(text):
    return GoogleTranslator(source='th', target='en').translate(text)

def get_nutrition_info(food_text):
    query = translate_to_english(food_text)
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    response = requests.post(url, headers=HEADERS, json={"query": query})

    if response.status_code != 200:
        print("ดึงข้อมูลอาหารไม่สำเร็จ:", response.status_code)
        return None

    foods = response.json().get("foods", [])
    if not foods:
        print("ไม่พบข้อมูลอาหาร")
        return None

    total_protein = sum(f.get("nf_protein", 0) for f in foods)
    total_fat = sum(f.get("nf_total_fat", 0) for f in foods)
    total_carbs = sum(f.get("nf_total_carbohydrate", 0) for f in foods)
    total_calories = sum(f.get("nf_calories", 0) for f in foods)
    


    return {
        "protein": total_protein,
        "fat": total_fat,
        "carbs": total_carbs,
        "calories": total_calories
    }



def get_exercise_info(activity_text, weight_kg, height_cm, age, gender):
    query = translate_to_english(activity_text)
    url = "https://trackapi.nutritionix.com/v2/natural/exercise"
    response = requests.post(url, headers=HEADERS, json={
        "query": query, "gender": gender,
        "weight_kg": weight_kg, "height_cm": height_cm, "age": age
    })
    exercises = response.json().get("exercises", []) 
    total = sum(e["nf_calories"] for e in exercises)
    return total
