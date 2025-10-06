# modules/ConnectDatabase.py
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def connect():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        sslmode=os.getenv("DB_SSLMODE", "require")
    )
    cursor = conn.cursor()
    return cursor, conn


# -----------------------------
# USER TABLE
# -----------------------------
insert_user = """
INSERT INTO "user" (name, weight, height, age, gender, goal, username, password, activity_level)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

update_user = """UPDATE "user" SET weight=%s, height=%s, goal=%s WHERE userid=%s"""
delete_user = """DELETE FROM "user" WHERE userid=%s"""
select_user = """SELECT * FROM "user" """


# -----------------------------
# ACTIVITY TABLE
# -----------------------------
insert_activity = """
INSERT INTO activity (activity_type, activity_name, activity_datetime, protein, carbohydrate, fat, calories, userid)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

update_activity = """UPDATE activity SET activity_name=%s, calories=%s WHERE activity_id=%s"""
delete_activity = """DELETE FROM activity WHERE activity_id=%s"""
select_activity = """SELECT * FROM activity"""


# -----------------------------
# CRUD FUNCTIONS
# -----------------------------
def insert_data(cursor, conn, query, data):
    cursor.execute(query, data)
    conn.commit()

def update_data(cursor, conn, query, data):
    cursor.execute(query, data)
    conn.commit()

def delete_data(cursor, conn, query, data):
    cursor.execute(query, data)
    conn.commit()

def select_all(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

def get_user_by_login(cursor, username, password):
    query = """SELECT userid, name FROM "user" WHERE username=%s AND password=%s"""
    cursor.execute(query, (username, password))
    return cursor.fetchone()

def close(cursor, conn):
    cursor.close()
    conn.close()


# -----------------------------
# REPORT / SUMMARY FUNCTIONS
# -----------------------------
def get_summary_last_7_days(cursor, user_id):
    seven_days_ago = (datetime.now() - timedelta(days=7)).date()
    query = """
        SELECT activity_type, activity_name, calories, activity_datetime
        FROM activity
        WHERE userid=%s AND activity_datetime::date >= %s
        ORDER BY activity_datetime
    """
    cursor.execute(query, (user_id, seven_days_ago))
    return cursor.fetchall()


def get_summary_by_date(cursor, user_id, date_input):
    query = """
        SELECT activity_type, activity_name, calories, activity_datetime
        FROM activity
        WHERE userid=%s AND activity_datetime::date = %s
        ORDER BY activity_datetime
    """
    cursor.execute(query, (user_id, date_input))
    return cursor.fetchall()


def get_summary_by_range(cursor, user_id, start_date, end_date):
    query = """
        SELECT activity_type, activity_name, calories, activity_datetime
        FROM activity
        WHERE userid=%s 
        AND activity_datetime::date BETWEEN %s AND %s
        ORDER BY activity_datetime
    """
    cursor.execute(query, (user_id, start_date, end_date))
    return cursor.fetchall()


def get_weekly_summary(user_id):
    cursor, conn = connect()
    query = """
        SELECT 
            DATE(activity_datetime) AS day,
            activity_type,
            SUM(calories) AS total_cal,
            SUM(protein) AS total_protein,
            SUM(carbohydrate) AS total_carb,
            SUM(fat) AS total_fat
        FROM activity
        WHERE userid = %s 
          AND activity_datetime >= (CURRENT_DATE - INTERVAL '7 days')
        GROUP BY DATE(activity_datetime), activity_type
        ORDER BY day ASC;
    """
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    close(cursor, conn)
    return rows
