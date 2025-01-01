import zipfile
import tempfile
import lxml.etree as ET
from typing import Optional, List
import os
from os.path import join
from .types.club import Club
from .types.session import Session
from .types.event import Event, SwimStyle, TimeStandardRef
from .types.athlete import Athlete
from .types.entry import Entry
from .utils import parse_dt, parse_time


class BaseApi:
    sessions: List[Session]
    events: List[Event]
    clubs: List[Club]
    athletes: List[Athlete]

    def __init__(self, filename: str, folder: Optional[str] = None):
        self.filename = filename
        self.folder = folder if folder is not None else os.curdir
        self.read()
        self.parse()

    def create_club(self, name: str) -> Club:
        eclub = ET.Element("CLUB", {"name": name})
        self.element_clubs.append(eclub)

        econtact = ET.Element("CONTACT", {"name": name})
        eclub.append(econtact)

        eathletes = ET.Element("ATHLETES")
        eclub.append(eathletes)

        club = Club(self, eclub, name)
        self.clubs.append(club)
        return club

    def parse(self):
        self.meet = self.root.find("MEETS").find("MEET")

        self.element_clubs = self.meet.find("CLUBS")
        if self.element_clubs is None:
            self.element_clubs = ET.Element("CLUBS")
            self.meet.append(self.element_clubs)
        self.preclubs = self.element_clubs.findall("CLUB")
        self.clubs = []
        self.athletes = []
        for eclub in self.preclubs:
            club = Club(
                self,
                eclub,
                eclub.get("name"),
                eclub.get("nation"),
                eclub.find("CONTACT").attrib,
            )

            preathletes_el = eclub.find("ATHLETES")
            if preathletes_el is None:
                preathletes_el = ET.Element("ATHLETES")
                eclub.append(preathletes_el)

            athletes = []
            preathletes = preathletes_el.findall("ATHLETE")
            for eathlete in preathletes:
                preentries_el = eathlete.find("ENTRIES")
                if preentries_el is None:
                    preentries_el = ET.Element("ENTRIES")
                    eathlete.append(preentries_el)

                preentries = preentries_el.findall("ENTRY")
                entries = []
                for eentry in preentries:
                    entry = Entry(
                        self,
                        eentry,
                        int(eentry.get("eventid")),
                        parse_time(eentry.get("entrytime")),
                    )
                    entries.append(entry)

                athlete = Athlete(
                    self,
                    eathlete,
                    club,
                    eathlete.get("lastname"),
                    eathlete.get("firstname"),
                    parse_dt(eathlete.get("birthdate")),
                    eathlete.get("gender"),
                    int(eathlete.get("athleteid")),
                    eathlete.get("license"),
                    entries
                )
                self.athletes.append(athlete)
                athletes.append(athlete)
            club.athletes = athletes
            self.clubs.append(club)

        self.element_sessions = self.meet.find("SESSIONS")
        self.presessions = self.element_sessions.findall("SESSION")
        self.sessions = []
        self.events = []
        for esession in self.presessions:
            dt = parse_dt(esession.get("date"), esession.get("daytime"))
            preevents = esession.find("EVENTS").findall("EVENT")
            events = []
            for eevent in preevents:
                pss = eevent.find("SWIMSTYLE")
                ss = SwimStyle(
                    pss,
                    int(pss.get("distance")),
                    int(pss.get("relaycount")),
                    pss.get("stroke"),
                )

                etsr = eevent.find("TIMESTANDARDREFS")
                licenses = etsr.findall("TIMESTANDARDREF")
                standart_list = []
                for l in licenses:
                    tmr = TimeStandardRef(
                        l, 
                        l.get("marker"),
                        int(l.get("timestandardlistid"))
                    )
                    standart_list.append(tmr)

                event = Event(
                    self,
                    eevent,
                    int(eevent.get("eventid")),
                    eevent.get("gender"),
                    int(eevent.get("number")),
                    int(eevent.get("order")),
                    eevent.get("round"),
                    int(eevent.get("preeventid", -1)),
                    ss,
                    standart_list,
                )
                events.append(event)
                self.events.append(event)
            session = Session(
                self,
                esession,
                dt,
                esession.get("name"),
                int(esession.get("number")),
                events,
            )
            self.sessions.append(session)

    def get_count_alts(self) -> int:
        return len(self.athletes)

    def read(self):
        with zipfile.ZipFile(self.filename) as zp:
            if len(zp.filelist) != 1:
                raise TypeError("Incorrect len file")
            with zp.open(zp.filelist[0]) as file:
                inf = file.read()
                try:
                    self.root = ET.fromstring(inf)
                except ET.XMLSyntaxError:
                    self.root = ET.fromstring(inf.decode('Windows-1251'))

    def save(self, filename: Optional[str] = None):
        with zipfile.ZipFile(self.filename) as zp:
            zipinfo = zp.filelist[0]

        filename_lxf = filename + ".lxf"
        xml_string = ET.tostring(
            self.root,
            encoding='unicode',
            method="xml"
        )
        with open(join(self.folder, "result.xml"), "w+") as ft:
            ft.write(xml_string)

        with tempfile.TemporaryDirectory() as dir:
            path = join(dir, zipinfo.filename)

            with open(path, "w+") as f:
                f.write(xml_string)

            with zipfile.ZipFile(
                filename_lxf, "w", compression=zipfile.ZIP_DEFLATED
            ) as zf:
                zf.write(path, zipinfo.filename)
                # zf.writestr(zipinfo, xml_string)

    def __repr__(self):
        return f"<{type(self).__name__} filename={self.filename}>"
