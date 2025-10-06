def show_weekly_report(weekly_data, tdee):
    print("\n=== 🧾 สรุปสัปดาห์ ===")
    total_net = sum(d["net"] for d in weekly_data)
    print(f"รวมพลังงานสุทธิ 7 วัน: {total_net:.0f} kcal")
    print(f"เฉลี่ยต่อวัน: {total_net / 7:.0f} kcal")
    print(f"TDEE ต่อวัน: {tdee:.0f} kcal")
    print("\nรายละเอียดรายวัน:")
    for d in weekly_data:
        print(f"วัน {d['day']}: กิน {d['eat']:.0f} | เผา {d['burn']:.0f} | สุทธิ {d['net']:.0f}")


def show_summary_report(rows, title):
    """แสดงผลรวมอาหาร/กิจกรรม"""
    if not rows:
        print(f"ไม่พบข้อมูล {title}")
        return

    total_eat = 0
    total_burn = 0
    print(f"\n=== 🗓️ {title} ===")
    for activity_type, activity_name, calories, activity_datetime in rows:
        if activity_type == "eat":
            total_eat += calories
            tag = "🍽️"
        else:
            total_burn += abs(calories)
            tag = "🏃"
        print(f"{tag} {activity_name} — {calories:.0f} kcal ({activity_datetime})")

    net = total_eat - total_burn
    print("\n📊 สรุปผลรวม:")
    print(f"กินทั้งหมด: {total_eat:.0f} kcal")
    print(f"เผาผลาญทั้งหมด: {total_burn:.0f} kcal")
    print(f"พลังงานสุทธิ: {net:.0f} kcal\n")


