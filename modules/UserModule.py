from flask import session, flash, redirect, url_for
from .ConnectDatabase import connect
import re
def login_user(form):
    """ตรวจสอบการเข้าสู่ระบบ"""
    username = form["username"]
    password = form["password"]

    cursor, conn = connect()
    cursor.execute(
        "SELECT userid, name, password, weight, height, age, gender, goal, activity_level FROM user WHERE username=%s",
        (username,)
    )
    row = cursor.fetchone()

    if row and row[2] == password:
        session["userid"] = row[0]
        session["name"] = row[1]
        session["weight"] = float(row[3]) if row[3] else 0
        session["height"] = float(row[4]) if row[4] else 0
        session["age"] = int(row[5]) if row[5] else 0
        session["gender"] = row[6]
        session["goal"] = (row[7])
        session["activity_level"] = row[8]
        flash(f"ยินดีต้อนรับ {session['name']}", "success")
        next_page = "dashboard"
    else:
        flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง", "danger")
        next_page = "login"

    cursor.close()
    conn.close()
    return redirect(url_for(next_page))


def register_user(form):
    """ลงทะเบียนผู้ใช้ใหม่"""
    name = form["name"]
    weight = float(form["weight"])
    height = float(form["height"])
    age = int(form["age"])
    gender = form["gender"]
    goal = form["goal"]
    username = form["username"]
    password = form["password"]
    activity_level = int(form["activity_level"])

    if not re.match(r"^[A-Za-z0-9_]{3,20}$", username):
        flash("ชื่อผู้ใช้ต้องเป็นภาษาอังกฤษ (a-z, A-Z, 0-9, _) ความยาว 3-20 ตัวอักษร", "warning")
        return redirect(url_for("register"))

    if not re.match(r"^[A-Za-z0-9@#$%^&+=!]{6,20}$", password):
        flash("รหัสผ่านต้องเป็นภาษาอังกฤษ (6-20 ตัวอักษร) และใช้สัญลักษณ์พื้นฐานได้", "warning")
        return redirect(url_for("register"))
    
    cursor, conn = connect()
    try:
        cursor.execute("""
            INSERT INTO user (name, weight, height, age, gender, goal, username, password, activity_level)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (name, weight, height, age, gender, goal, username, password, activity_level))
        conn.commit()
        flash("สมัครสมาชิกสำเร็จ — กรุณาเข้าสู่ระบบ", "success")
    except Exception as e:
        conn.rollback()
        flash("ไม่สามารถสมัครสมาชิกได้ — username อาจซ้ำ หรือเกิดข้อผิดพลาด", "danger")
    finally:
        cursor.close()
        conn.close()


def logout_user():
    """ออกจากระบบผู้ใช้"""
    # ลบข้อมูลทั้งหมดใน session
    session.clear()
    flash("ออกจากระบบเรียบร้อยแล้ว", "info")
    return redirect(url_for("login"))

def get_user_profile(userid):
    cursor, conn = connect()
    cursor.execute("""
        SELECT name, weight, height, age, gender, goal, username, activity_level 
        FROM user WHERE userid = %s
    """, (userid,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_user_profile(userid, name, weight, height, age, gender, goal, username, activity_level):
    """อัปเดตข้อมูลผู้ใช้ โดยตรวจสอบ username"""
    # --- ตรวจสอบรูปแบบ username ---
    if not re.match(r"^[A-Za-z0-9_]{3,20}$", username):
        flash("ชื่อผู้ใช้ต้องเป็นภาษาอังกฤษ (a-z, A-Z, 0-9, _) ความยาว 3-20 ตัวอักษร", "warning")
        return False

    cursor, conn = connect()
    try:
        # --- ตรวจสอบว่า username ซ้ำกับคนอื่นหรือไม่ ---
        cursor.execute("SELECT userid FROM user WHERE username = %s AND userid != %s", (username, userid))
        if cursor.fetchone():
            flash("ชื่อผู้ใช้นี้ถูกใช้แล้ว กรุณาเลือกชื่ออื่น", "danger")
            cursor.close()
            conn.close()
            return False

        # --- บันทึกการอัปเดตข้อมูล ---
        cursor.execute("""
            UPDATE user 
            SET name=%s, weight=%s, height=%s, age=%s, gender=%s, goal=%s, username=%s, activity_level=%s
            WHERE userid=%s
        """, (name, weight, height, age, gender, goal, username, activity_level, userid))

        conn.commit()
        flash("อัปเดตข้อมูลผู้ใช้เรียบร้อยแล้ว", "success")
        return True

    except Exception as e:
        conn.rollback()
        flash(f"เกิดข้อผิดพลาดในการอัปเดตข้อมูล: {e}", "danger")
        return False

    finally:
        cursor.close()
        conn.close()
