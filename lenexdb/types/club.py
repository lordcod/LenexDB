from __future__ import annotations
from xml.etree.ElementTree import Element
from typing import TYPE_CHECKING, Optional, List
from dataclasses import dataclass, field
from datetime import datetime

if TYPE_CHECKING:
    from ..baseapi import BaseApi
    from .athlete import Athlete


@dataclass
class Club:
    baseapi: BaseApi
    element: Element
    name: str
    nation: Optional[str] = None
    contact: Optional[dict] = None
    athletes: List[Athlete] = field(init=False)
    
    def __post_init__(self):
        self.athletes = []
    
    def create_athlete(
        self, lastname: str, firstname: str, birthdate: datetime | str, gender: str
    ):
        from .athlete import Athlete
        count = self.baseapi.get_count_alts()
        eathlete = Element(
            "ATHLETE",
            {
                "lastname": lastname,
                "firstname": firstname,
                "birthdate": birthdate.strftime("%Y-%m-%d") if isinstance(birthdate, datetime) else birthdate,
                "gender": gender,
                "athleteid": str(count + 1),
            },
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
            [],
        )
        self.athletes.append(athlete)
        self.baseapi.athletes.append(athlete)
        return athlete
