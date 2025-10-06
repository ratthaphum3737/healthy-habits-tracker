def calculate_bmi(weight_kg, height_cm):
    return weight_kg / ((height_cm / 100) ** 2)

def calculate_bmr(weight_kg, height_cm, age, gender):
    if gender.lower() == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def calculate_tdee(bmr, activity_level):
    multiplier = {1:1.2, 2:1.375, 3:1.55, 4:1.725, 5:1.9}
    return bmr * multiplier.get(activity_level, 1.2)
