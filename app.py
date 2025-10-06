from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from modules.ConnectDatabase import connect, get_weekly_summary
from modules.NutritionixModule import get_nutrition_info, get_exercise_info
from modules.CalculationModule import calculate_bmi, calculate_bmr, calculate_tdee
from modules.DashboardModule import show_dashboard
from modules.UserModule import register_user, login_user, logout_user, get_user_profile, update_user_profile
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "replace-with-your-secret-key"


@app.route("/")
def index():
    if "userid" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        register_user(request.form)
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return login_user(request.form)
    return render_template("login.html")


@app.route("/logout")
def logout():
    return logout_user()


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "userid" not in session:
        return redirect(url_for("login"))

    userid = session["userid"]

    if request.method == "POST":
        name = request.form["name"]
        weight = request.form["weight"]
        height = request.form["height"]
        age = request.form["age"]
        gender = request.form["gender"]
        goal = request.form["goal"]
        username = request.form["username"]
        activity_level = request.form["activity_level"]

        update_user_profile(userid, name, weight, height, age, gender, goal, username, activity_level)
        return redirect(url_for("dashboard"))

    user = get_user_profile(userid)
    return render_template("edit_profile.html", user=user)


@app.route("/dashboard")
def dashboard():
    return show_dashboard()


@app.route("/add_food", methods=["GET", "POST"])
def add_food():
    if "userid" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        food_text = request.form["food_text"]
        time_option = request.form.get("time_option")
        if time_option == "now":
            activity_time = datetime.now()
        else:
            activity_time = request.form.get("custom_datetime")

        nutrition = get_nutrition_info(food_text)
        calories = nutrition.get("calories") if nutrition else 0
        protein = nutrition.get("protein") if nutrition else 0
        carbs = (nutrition.get("carbohydrate") or 0) if nutrition else 0
        fat = nutrition.get("fat") if nutrition else 0

        if calories == 0 and protein == 0 and carbs == 0 and fat == 0:
            flash("อาหารไม่ถูกต้องหรือไม่มีสารอาหาร", "danger")
            return render_template("add_food.html")

        cursor, conn = connect()
        cursor.execute("""
            INSERT INTO activity (userid, activity_type, activity_name, calories, protein, carbohydrate, fat, activity_datetime)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (session["userid"], "eat", food_text, calories, protein, carbs, fat, activity_time))
        conn.commit()
        cursor.close(); conn.close()
        flash("บันทึกอาหารเรียบร้อย", "success")
        return redirect(url_for("dashboard"))
    return render_template("add_food.html")


@app.route("/add_exercise", methods=["GET", "POST"])
def add_exercise():
    if "userid" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        act_text = request.form["act_text"]
        time_option = request.form.get("time_option")
        if time_option == "now":
            activity_time = datetime.now()
        else:
            activity_time = request.form.get("custom_datetime")

        burn = get_exercise_info(
            act_text,
            session.get("weight") or 70,
            session.get("height") or 170,
            session.get("age") or 30,
            session.get("gender") or "male"
        )
        if burn == 0:
            flash("กิจกรรมไม่ถูกต้อง", "danger")
            return render_template("add_exercise.html")

        cursor, conn = connect()
        cursor.execute("""
            INSERT INTO activity (userid, activity_type, activity_name, calories, protein, carbohydrate, fat, activity_datetime)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (session["userid"], "exercise", act_text, burn, 0, 0, 0, activity_time))
        conn.commit()
        cursor.close(); conn.close()
        flash("บันทึกกิจกรรมเรียบร้อย", "success")
        return redirect(url_for("dashboard"))
    return render_template("add_exercise.html")


@app.route("/report", methods=["GET", "POST"])
def report():
    if "userid" not in session:
        return redirect(url_for("login"))

    rows = []
    title = ""
    cursor, conn = connect()
    if request.method == "POST":
        mode = request.form.get("mode")
        if mode == "7days":
            cursor.execute("""
                SELECT activity_type, activity_name, calories, activity_datetime 
                FROM activity 
                WHERE userid=%s 
                AND activity_datetime >= CURRENT_DATE - INTERVAL '7 day' 
                ORDER BY activity_datetime DESC
            """, (session["userid"],))
            rows = cursor.fetchall()
            title = "สรุปผลรวมย้อนหลัง 7 วัน"
        elif mode == "bydate":
            date_input = request.form.get("date_input")
            cursor.execute("""
                SELECT activity_type, activity_name, calories, activity_datetime 
                FROM activity 
                WHERE userid=%s AND DATE(activity_datetime)=%s 
                ORDER BY activity_datetime DESC
            """, (session["userid"], date_input))
            rows = cursor.fetchall()
            title = f"สรุปผลวันที่ {date_input}"
        elif mode == "range":
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            cursor.execute("""
                SELECT activity_type, activity_name, calories, activity_datetime 
                FROM activity 
                WHERE userid=%s 
                AND DATE(activity_datetime) BETWEEN %s AND %s 
                ORDER BY activity_datetime DESC
            """, (session["userid"], start_date, end_date))
            rows = cursor.fetchall()
            title = f"สรุปผลจาก {start_date} ถึง {end_date}"

    cursor.close(); conn.close()
    return render_template("report.html", rows=rows, title=title)


@app.route("/manage_activity")
def manage_activity():
    if "userid" not in session:
        return redirect(url_for("login"))

    cursor, conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        SELECT activity_id AS id, activity_type, activity_name, calories, protein, carbohydrate, fat,
               TO_CHAR(activity_datetime, 'YYYY-MM-DD HH24:MI') AS activity_datetime
        FROM activity
        WHERE userid=%s
        ORDER BY activity_datetime DESC
    """, (session["userid"],))
    activities = cursor.fetchall()
    cursor.close(); conn.close()

    return render_template("manage_activity.html", activities=activities)


@app.route("/edit_activity/<int:id>", methods=["GET", "POST"])
def edit_activity(id):
    if "userid" not in session:
        return redirect(url_for("login"))
    cursor, conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == "POST":
        activity_type = request.form["activity_type"]
        name = request.form["activity_name"]
        calories = request.form["calories"]
        protein = request.form["protein"]
        carbs = request.form["carbohydrate"]
        fat = request.form["fat"]
        dt = request.form["activity_datetime"]

        cursor.execute("""
            UPDATE activity
            SET activity_type=%s, activity_name=%s, calories=%s, protein=%s, carbohydrate=%s, fat=%s, activity_datetime=%s
            WHERE activity_id=%s AND userid=%s
        """, (activity_type, name, calories, protein, carbs, fat, dt, id, session["userid"]))
        conn.commit()
        cursor.close(); conn.close()
        flash("อัปเดตรายการเรียบร้อย", "success")
        return redirect(url_for("manage_activity"))

    cursor.execute("""
        SELECT activity_id AS id, activity_type, activity_name, calories, protein, carbohydrate, fat,
               TO_CHAR(activity_datetime, 'YYYY-MM-DD HH24:MI') AS activity_datetime
        FROM activity
        WHERE activity_id=%s AND userid=%s
    """, (id, session["userid"]))
    act = cursor.fetchone()
    cursor.close(); conn.close()

    if not act:
        flash("ไม่พบกิจกรรมนี้", "danger")
        return redirect(url_for("manage_activity"))

    return render_template("edit_activity.html", act=act)


@app.route("/delete_activity/<int:id>")
def delete_activity(id):
    if "userid" not in session:
        return redirect(url_for("login"))
    cursor, conn = connect()
    cursor.execute("DELETE FROM activity WHERE activity_id=%s AND userid=%s", (id, session["userid"]))
    conn.commit()
    cursor.close(); conn.close()
    flash("ลบกิจกรรมเรียบร้อย", "success")
    return redirect(url_for("manage_activity"))


if __name__ == "__main__":
    app.run(debug=True)
