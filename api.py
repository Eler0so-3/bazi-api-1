from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from lunar_python import Solar

app = FastAPI()

class BirthData(BaseModel):
    birth_date: str  # формат: dd.mm.yyyy
    birth_time: str = "00.12"  # формат: mm.hh

@app.post("/")
async def get_bazi(data: BirthData):
    try:
        day, month, year = map(int, data.birth_date.strip().split("."))
        minute, hour = map(int, data.birth_time.strip().split("."))
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        eight_char = solar.getLunar().getEightChar()

        # Столпы
        year_pillar = eight_char.getYear()
        month_pillar = eight_char.getMonth()
        day_pillar = eight_char.getDay()
        hour_pillar = eight_char.getTime()

        # Извлечение информации
        def extract(pillar):
            stem = pillar[0]
            branch = pillar[1]
            element = {
                "甲": "Дерево", "乙": "Дерево",
                "丙": "Огонь", "丁": "Огонь",
                "戊": "Земля", "己": "Земля",
                "庚": "Металл", "辛": "Металл",
                "壬": "Вода", "癸": "Вода"
            }[stem]
            yin_yang = "Ян" if stem in "甲丙戊庚壬" else "Инь"
            animal = {
                "子": "Крыса", "丑": "Бык", "寅": "Тигр", "卯": "Кролик",
                "辰": "Дракон", "巳": "Змея", "午": "Лошадь", "未": "Коза",
                "申": "Обезьяна", "酉": "Петух", "戌": "Собака", "亥": "Свинья"
            }[branch]
            return {
                "pillar": pillar,
                "element": element,
                "yinyang": yin_yang,
                "animal": animal
            }

        year = extract(year_pillar)
        month = extract(month_pillar)
        day = extract(day_pillar)
        hour = extract(hour_pillar)

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

            "element_self": day["element"],
            "element": day["element"],
            "yin_yang": day["yinyang"]
        }

    except Exception as e:
        return {"error": str(e)}
