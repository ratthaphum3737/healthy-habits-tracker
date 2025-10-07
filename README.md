# 🩺 Healthy Habits Tracker

**Healthy Habits Tracker**  
เป็นเว็บแอปพลิเคชันที่พัฒนาด้วย **Flask Framework** สำหรับติดตามและวิเคราะห์พฤติกรรมสุขภาพของผู้ใช้ เช่น การรับประทานอาหาร การออกกำลังกาย และการตั้งเป้าหมายด้านสุขภาพ  
โปรแกรมนี้ช่วยให้ผู้ใช้เข้าใจพฤติกรรมสุขภาพของตนเองได้ดีขึ้น และปรับปรุงให้มีสุขภาพที่ดีขึ้นในระยะยาว

---

## 🚀 คุณสมบัติ (Features)

- 🧍‍♂️ **ระบบผู้ใช้ (User Management)**
  - ลงทะเบียน / เข้าสู่ระบบ / ออกจากระบบ
  - แก้ไขข้อมูลส่วนตัวของผู้ใช้
  - เก็บข้อมูลการใช้งานลงฐานข้อมูล

- 🍎 **โภชนาการ (Nutrition Tracking)**
  - ค้นหาข้อมูลอาหารผ่าน **Nutritionix API**
  - บันทึกและคำนวณปริมาณแคลอรี่ที่บริโภคต่อวัน
  - แสดงข้อมูลโภชนาการที่สำคัญ เช่น โปรตีน ไขมัน คาร์โบไฮเดรต

- 📊 **แดชบอร์ด (Dashboard)**
  - แสดงข้อมูลสรุปพฤติกรรมสุขภาพของผู้ใช้
  - แสดงเปรียบเทียบกับเป้าหมายที่ผู้ใช้ตั้งไว้
  - มีกราฟและสถิติเพื่อให้เห็นแนวโน้มสุขภาพ

- 🧮 **คำนวณทางสุขภาพ (Health Calculation)**
  - คำนวณค่า **BMI**, **BMR**, และพลังงานที่ควรบริโภคต่อวัน
  - ช่วยผู้ใช้กำหนดเป้าหมายที่เหมาะสมกับร่างกาย

- 📋 **รายงานการกิน (Reports)**
  - สร้างรายงานสรุปพฤติกรรมการกิน
  - แสดงผลในรูปแบบกราฟ / ตาราง
  - แสดงแนวโน้มการกินของผู้ใช้ตามช่วงเวลา

- 🗄️ **ฐานข้อมูล (Database)**
  - จัดเก็บข้อมูลผู้ใช้, ประวัติอาหาร, การออกกำลังกาย และเป้าหมาย
  - ใช้งานผ่านโมดูล `ConnectDatabase.py` ซึ่งรองรับ SQLite หรือ MySQL

---

## 🧩 โครงสร้างโปรเจกต์ (Project Structure)

<div align="left">

<pre>
healthy_habits_tracker/
│
├── <b>app.py</b>                      จุดเริ่มต้นของ Flask Application
├── <b>requirements.txt</b>            ไลบรารีที่ใช้ในโปรเจกต์
│
└── <b>modules/</b>
    ├── CalculationModule.py    ฟังก์ชันคำนวณสุขภาพ
    ├── ConnectDatabase.py      จัดการฐานข้อมูล
    ├── DashboardModule.py      สร้างแดชบอร์ด
    ├── NutritionixModule.py    ดึงข้อมูลจาก Nutritionix API
    ├── ReportModule.py         สร้างรายงานสุขภาพ
    ├── UserModule.py           จัดการผู้ใช้
    └── __init__.py
</pre>

</div>

---

## ⚙️ Installation & Usage

### 1️⃣ Clone the project

```bash
git clone https://github.com/DEW177/healthy_habits_tracker.git
cd healthy_habits_tracker
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Create `.env` file

ใช้เก็บ API Key และ Secret Key ต่าง ๆ

ตัวอย่าง:

```
FLASK_ENV=development
SECRET_KEY=your_secret_key
NUTRITIONIX_APP_ID=your_app_id
NUTRITIONIX_API_KEY=your_api_key
DATABASE_URL=sqlite:///healthy_habits.db
```

### 4️⃣ Run Flask app

```bash
python app.py
```

จากนั้นเปิดเว็บเบราว์เซอร์ไปที่
👉 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📦 Dependencies

| Library             | Description                               |
| ------------------- | ----------------------------------------- |
| **Flask**           | Web Framework หลักของระบบ                 |
| **Requests**        | ใช้เชื่อมต่อ Nutritionix API              |
| **Jinja2**          | Template engine สำหรับแสดงผลหน้าเว็บ      |
| **SQLite3 / MySQL** | ฐานข้อมูลเก็บข้อมูลผู้ใช้และกิจกรรม       |
| **dotenv**          | โหลดค่าตัวแปรจากไฟล์ `.env`               |
| **Nutritionix API** | ดึงข้อมูลโภชนาการจากฐานข้อมูลอาหารออนไลน์ |

---

## 🧠 Concept

> “Good habits lead to better health.”

แนวคิดของโปรเจกต์นี้คือใช้เทคโนโลยีมาช่วยติดตาม
และสร้างแรงจูงใจให้ผู้ใช้รักษาพฤติกรรมสุขภาพที่ดี
ผ่านข้อมูลที่แสดงผลในรูปแบบกราฟและรายงานอย่างเข้าใจง่าย

---

## 📜 Example Workflow

1. ผู้ใช้สมัครสมาชิก / เข้าสู่ระบบ
2. บันทึกอาหารที่รับประทานในแต่ละวัน
3. ระบบคำนวณปริมาณแคลอรี่และสารอาหาร
4. แสดงข้อมูลบน Dashboard
5. ผู้ใช้สามารถดูรายงานสรุปแนวโน้มสุขภาพได้

---

## 👨‍💻 Developers

**Healthy Habits Tracker Team**
College of Computing

* นาย รัฐภูมิ แฝงฤทธิ์หลง
* นาย กิตติพัฒน์ สีราช

Developed for educational purposes.

---

## 📜 License

Distributed under the **MIT License**
สามารถใช้งานและปรับปรุงเพื่อการศึกษาและพัฒนาเพิ่มเติมได้

---





WEBSITE : https://healthy-habits-tracker.onrender.com
