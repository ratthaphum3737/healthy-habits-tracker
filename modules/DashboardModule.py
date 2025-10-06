from flask import session, request, redirect, url_for, render_template
from .CalculationModule import calculate_bmi, calculate_bmr, calculate_tdee
from .ConnectDatabase import get_weekly_summary


def show_dashboard():
    if "userid" not in session:
        return redirect(url_for("login"))

    weight = session.get("weight", 70)
    height = session.get("height", 170)
    age = session.get("age", 30)
    gender = session.get("gender", "male")
    activity_level = session.get("activity_level",1)
    
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)

    # --- ดึงข้อมูลย้อนหลัง 7 วัน ---
    data = get_weekly_summary(session["userid"])

    days, eat_cal, exercise_cal = [], [], []
    protein, carbs, fat = [], [], []

    unique_days = sorted(list(set([row[0] for row in data])))

    for d in unique_days:
        days.append(d.strftime("%d/%m"))
        eat_row = next((r for r in data if r[0] == d and r[1] == "eat"), None)
        ex_row = next((r for r in data if r[0] == d and r[1] == "exercise"), None)
        eat_cal.append(eat_row[2] if eat_row else 0)
        exercise_cal.append(ex_row[2] if ex_row else 0)
        protein.append(eat_row[3] if eat_row else 0)
        carbs.append(eat_row[4] if eat_row else 0)
        fat.append(eat_row[5] if eat_row else 0)

    # --- ปรับค่า TDEE ตามพลังงานที่เผาออกเฉลี่ย ---
    extra_burn = sum(exercise_cal) / len(exercise_cal) if exercise_cal else 0
    adj_tdee = tdee + float(extra_burn)

    # --- ค่าที่ควรได้รับต่อวัน ---
    target = {
        "cal": adj_tdee,
        "protein": weight * 1.6,
        "carb": weight * 4,
        "fat": weight * 1
    }

    return render_template("dashboard.html",
                           bmi=bmi, bmr=bmr, tdee=adj_tdee,
                           activity_level=activity_level,
                           days=days,
                           eat_cal=eat_cal,
                           exercise_cal=exercise_cal,
                           protein=protein,
                           carbs=carbs,
                           fat=fat,
                           target=target)
