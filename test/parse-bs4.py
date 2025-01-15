import requests
from bs4 import BeautifulSoup
import json

def get_url(page: str | int):
    return f"https://swimmasters.ru/tools/base_times?page={page}?utf8=%E2%9C%93&q%5Byear_eq%5D=2025&q%5Bdiscipline_id_eq%5D=&q%5Bgender_eq%5D=&q%5Bage_group_eq%5D=&q%5Bcourse_eq%5D="


def get_html(url: str) -> str:
    return requests.get(url).text


def parse_doc(page: int):
    contents = []

    html_doc = get_html(get_url(page))
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find(id='object_list').find('table')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        els = [el.contents[0] for el in tr.find_all('td')]
        contents.append(els)
    return contents


global_content = []
i = 1
while True:
    content = parse_doc(i)
    global_content.extend(content)
    i += 1
    if not content:
        break

with open('masters_times.json', 'wb+') as f:
    f.write(json.dumps(global_content, ensure_ascii=False, indent=2).encode())
