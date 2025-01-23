import json
data = json.load(open('masters_times.json', 'rb'))
print(data)

text = """
Formula=CUBED_DSV
Id=1121
Name=FPM Master Table
Options=MASTER
ShortNameVersion=FPM Masters 16
Version=2025
Courses=LCM,SCM

course;gender;agemin;agemax;distance;stroke;mintime;relaycount
"""

courses = {
    '25 м': 'SCM',
    '50 м': 'LCM'
}
strokes = {
    "вольный стиль": "FREE",
    "на спине": "BACK",
    "брасс": "BREAST",
    "баттерфляй": "FLY",
    "комплексное плавание": "MEDLEY",
    "комбинированная": "MEDLEY"
}


def parse_distance(distance: str):
    if distance.startswith('Эстафета'):
        distance = distance.removeprefix('Эстафета ')
        dist, stroke = distance.split(' м ')
        dist, stroke = int(dist.removeprefix('4×')), strokes[stroke]
        return dist, stroke, 4
    else:
        dist, stroke = distance.split(' м ')
        dist, stroke = int(dist), strokes[stroke]
        return dist, stroke, 1


def parse_data(data: list):
    distance, ga, course, time = data
    course = courses[course]
    gender, (agemin, agemax) = ga[0], ga[1:].split('-')
    distance, stroke, relaycount = parse_distance(distance)
    if ':' not in time:
        time = '0:'+time
    result = ';'.join(
        map(str, [course, gender, agemin, agemax, distance, stroke, time, relaycount]))
    return result


for d in data:
    text += parse_data(d)+'\n'

with open('base_time.txt', 'wb+') as file:
    file.write(text.encode())
