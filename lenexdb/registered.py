from lenexdb.baseapi import BaseApi, Athlete, Club, Event
import json
import openpyxl
import re
from datetime import time, datetime


class RegisteredDistance:
    clubs: dict[str, Club] = dict()
    athletes: dict[str, Athlete] = dict()

    def __init__(self, xpath: str, table: str, data: dict):
        self.bapi = BaseApi(xpath, 'result')
        self.data = data
        self.config = data['location']
        self.registered = data['reversed_styles']

        workbook = openpyxl.load_workbook(table)
        self.sheet = workbook.active

    @classmethod
    def init(cls) -> 'RegisteredDistance':
        return cls.__new__(cls)

    @classmethod
    def base_init(cls, baseapi: BaseApi, table: str, data: dict | None = None) -> 'RegisteredDistance':
        self = cls.init()

        self.bapi = baseapi

        workbook = openpyxl.load_workbook(table)
        self.sheet = workbook.active

        if data is not None:
            self.data = data
            self.config = data['location']
            self.registered = data['reversed_styles']

        return self

    def add_elements(self):
        for club in self.bapi.clubs:
            self.clubs[club.name.lower()] = club
        for athlete in self.bapi.athletes:
            key = athlete.lastname + \
                " " + athlete.firstname
            self.athletes[key.lower()] = athlete

    def parse(self):
        for i in self.sheet.iter_rows():
            row = tuple(r.value for r in i)
            break
        for row_k in self.sheet.iter_rows(min_row=2):
            row = tuple(r.value for r in row_k)
            if row[self.config['lastname']] is None:
                break
            club = self.get_club(row[self.config['club']])
            try:
                event = self.find_swimstyle(
                    self.parse_gender(row[self.config['gender']]),
                    self.registered.get(row[self.config['stroke']]),
                    int(row[self.config['distance']])
                )
            except TypeError:
                print('Skip distance',
                      row[self.config['stroke']], row[self.config['distance']])
                continue
            athlete = self.get_athlete(club, event, row)
            et = self.parse_entrytime(row[self.config['entrytime']])
            athlete.add_entry(event.eventid, et)

    def parse_lisense(self, license: str) -> str:
        def chg(match: re.Match):
            t = match.string[match.regs[0][0]:match.regs[0][1]]
            return t.lower()
        license = re.sub('[^I]{1}', chg, license)

        for a, b in self.data['replacement'].items():
            license = license.replace(a, b)
        return license

    def get_lisense(self, event: Event, license: str | None) -> str | None:
        if license is None:
            return None
        license = self.parse_lisense(str(license))
        for ts in event.timestandardrefs:
            if ts.marker == license or license == 'IIIюн':
                return ts.marker
        print('Not found license', license)
        return None

    def parse_entrytime(self, entrytime) -> str:
        if isinstance(entrytime, (time, datetime)):
            r = entrytime.strftime('00:%H:%M.%S')
            return r
        m = re.fullmatch("(\d{1,3}):(\d{1,2}):(\d{1,2})", entrytime)
        if m is None:
            print('Incorrect entrytime', entrytime)
            return "00:00:00.00"
        return f"00:{m.group(1)}:{m.group(2)}.{m.group(3)}"

    def find_swimstyle(self, gdr, srk, dist) -> Event:
        for e in self.bapi.events:
            if (
                e.gender == gdr
                and e.swim_style.stroke == srk
                and e.swim_style.distance == dist
            ):
                return e
        raise TypeError("Incorrect distance")

    def parse_gender(self, gender: str):
        if gender == "Мужской":
            return "M"
        if gender == "Женский":
            return "F"
        raise TypeError("Sex not found")

    def parse_bd(self, bd: str):
        if not isinstance(bd, str):
            return bd
        dbl = bd.split(".")
        dbl.reverse()
        return "-".join(dbl)

    def get_club(self, name: str) -> Club:
        if name.lower() not in self.clubs:
            self.clubs[name.lower()] = self.bapi.create_club(name)
        return self.clubs[name.lower()]

    def get_athlete(self, club: Club, event: Event, row: tuple) -> Athlete:
        key = (row[self.config['lastname']]
               + " " + row[self.config['firstname']]).lower()
        if key not in self.athletes:
            athl = club.create_athlete(
                row[self.config['lastname']],
                row[self.config['firstname']],
                self.parse_bd(row[self.config['birthdate']]),
                self.parse_gender(row[self.config['gender']]),
                self.get_lisense(event, row[self.config['license']]),
            )
            self.athletes[key] = athl
        return self.athletes[key]


if __name__ == '__main__':
    data = json.load(open("data.json", "rb+"))
    xpath = r"C:\Users\2008d\Downloads\Telegram Desktop\20250209_Lenex.lxf"
    rd = RegisteredDistance(xpath, "test3.xlsx", data)
    rd.bapi.save("result/test.lxf")
    print(rd)
