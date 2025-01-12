a = {
    "lastname": 0,
    "firstname": 1,
    "gender": 2,
    "license": 3,
    "birthdate": 4,
    "club": 5,
    "stroke": 6,
    "distance": 7,
    "entrytime": 8
}
b = {
    "Фамилия": 0,
    "Имя": 1,
    "Пол": 2,
    "р": 3,
    "Дата рождения": 4,
    "Город": 5,
    "Дисциплина": 6,
    "Дистанция": 7,
    "Заявочное время": 8
}
import json
s = json.dumps(dict(zip(b.keys(), a.keys())), ensure_ascii=False)
print(s)