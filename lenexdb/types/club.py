from __future__ import annotations
from lxml.etree import Element
from typing import TYPE_CHECKING, Optional, List
from dataclasses import dataclass, field, InitVar
from datetime import datetime
from ._base_obj import BaseObj, selfname

if TYPE_CHECKING:
    from ..baseapi import BaseApi
    from .athlete import Athlete


def parse_contact(club: Club, contact: dict) -> None:
    el = club.element.find('CONTACT')
    el.attrib = contact

@dataclass
class Club(BaseObj):
    baseapi: BaseApi
    element: Element
    name: str = field(metadata={"ext": selfname})
    nation: Optional[str] = field(default=None, metadata={"ext": selfname})
    contact: Optional[dict] = field(default=None, metadata={"func": parse_contact})
    athletes: List[Athlete] = field(init=False)

    def __post_init__(self):
        self.athletes = []

    def create_athlete(
        self,
        lastname: str,
        firstname: str,
        birthdate: datetime | str,
        gender: str,
        license: str,
    ):
        from .athlete import Athlete

        count = self.baseapi.get_count_alts()
        attrib = {
            "lastname": lastname,
            "firstname": firstname,
            "birthdate": (
                birthdate.strftime("%Y-%m-%d")
                if isinstance(birthdate, datetime)
                else birthdate
            ),
            "gender": gender,
            "athleteid": str(count + 1),
        }
        if license:
            attrib["license"] = license

        eathlete = Element(
            "ATHLETE",
            attrib,
        )
        entries_el = Element("ENTRIES")
        eathlete.append(entries_el)
        self.element.find("ATHLETES").append(eathlete)
        athlete = Athlete(
            self.baseapi,
            eathlete,
            self,
            lastname,
            firstname,
            birthdate,
            gender,
            count + 1,
            license,
            [],
        )
        self.athletes.append(athlete)
        self.baseapi.athletes.append(athlete)
        return athlete
