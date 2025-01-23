import requests
from bs4 import BeautifulSoup
import json
import itertools

genders = {
    1: 'M',
    2: 'F',
    3: 'X'
}


def get_html(page: int, gender: int) -> str:
    url = f"https://swimmasters.ru/tools/base_times"
    params = {
        'utf8': '✓',
        'page': str(page),
        'q[year_eq]': '2025',
        'q[discipline_id_eq]': '',
        'q[gender_eq]': str(gender),
        'q[age_group_eq]': '',
        'q[course_eq]': '',
    }
    return requests.get(url, params=params).text


def parse_doc(page: int, gender: int):
    contents = []

    html_doc = get_html(page, gender)
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find(id='object_list').find('table')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        els = [el.contents[0] for el in tr.find_all('td')]
        if not els[1].startswith(genders[gender]):
            print('Invalid gender', els, genders[gender] + els[1][1:])
            els[1] = genders[gender] + els[1][1:]
        contents.append(els)
    return contents


global_content = []
for gender in genders:
    print(f'{gender=}')
    for i in itertools.count(start=1):
        print(f'{i=}')
        content = parse_doc(i, gender)
        global_content.extend(content)
        if not content:
            break

with open('masters_times.json', 'wb+') as f:
    f.write(json.dumps(global_content, ensure_ascii=False, indent=2).encode())
