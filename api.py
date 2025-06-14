from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from lunar_python import Solar

app = FastAPI()

class BirthData(BaseModel):
    birth_date: str
    birth_time: str = None  # теперь допускаем None

@app.post("/")
async def get_bazi(data: BirthData):
    try:
        print("=== Запрос получен ===")
        print("birth_date:", data.birth_date)
        print("birth_time:", data.birth_time)

        # Разбор даты
        day, month, year = map(int, data.birth_date.strip().split("."))

        # Разбор времени (в формате hh.mm), или подставляем 12:00
        if not data.birth_time or "." not in data.birth_time:
            hour, minute = 12, 0
        else:
            hour, minute = map(int, data.birth_time.strip().split("."))

        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()

        if not eight_char:
            return {"error": "EightChar is empty"}

        def extract(pillar):
            if not pillar:
                return {"pillar": "", "element": "", "yinyang": "", "animal": ""}
            stem = pillar[0]
            branch = pillar[1]
            element = {
                "甲": "Дерево", "乙": "Дерево",
                "丙": "Огонь", "丁": "Огонь",
                "戊": "Земля", "己": "Земля",
                "庚": "Металл", "辛": "Металл",
                "壬": "Вода", "癸": "Вода"
            }.get(stem, "")
            yin_yang = "Ян" if stem in "甲丙戊庚壬" else "Инь" if stem else ""
            animal = {
                "子": "Крыса", "丑": "Бык", "寅": "Тигр", "卯": "Кролик",
                "辰": "Дракон", "巳": "Змея", "午": "Лошадь", "未": "Коза",
                "申": "Обезьяна", "酉": "Петух", "戌": "Собака", "亥": "Свинья"
            }.get(branch, "")
            return {
                "pillar": pillar,
                "element": element,
                "yinyang": yin_yang,
                "animal": animal
            }

        year = extract(eight_char.getYear())
        month = extract(eight_char.getMonth())
        day = extract(eight_char.getDay())
        hour = extract(eight_char.getTime())

        print("RESULT:", year, month, day, hour)

        return {
            "pillar_year": year["pillar"],
            "year_element": year["element"],
            "year_yinyang": year["yinyang"],
            "year_animal": year["animal"],

            "pillar_month": month["pillar"],
            "month_element": month["element"],
            "month_yinyang": month["yinyang"],
            "month_animal": month["animal"],

            "pillar_day": day["pillar"],
            "day_element": day["element"],
            "day_yinyang": day["yinyang"],
            "day_animal": day["animal"],

            "pillar_hour": hour["pillar"],
            "hour_element": hour["element"],
            "hour_yinyang": hour["yinyang"],
            "hour_animal": hour["animal"],

            "element": day["element"],
            "element_self": day["element"],
            "yin_yang": day["yinyang"]
        }

    except Exception as e:
        print("Ошибка:", str(e))
        return {"error": str(e)}
