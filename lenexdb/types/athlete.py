from __future__ import annotations
from xml.etree.ElementTree import Element
from typing import TYPE_CHECKING, Optional, Literal, List
from dataclasses import dataclass
from datetime import datetime

if TYPE_CHECKING:
    from ..baseapi import BaseApi
    from .entry import Entry
    from .club import Club


@dataclass
class Athlete:
    baseapi: BaseApi
    element: Element
    club: Club
    lastname: str
    firstname: str
    birthdate: datetime
    gender: Literal["M", "F"]
    athleteid: int
    enries: List[Entry]

    def add_entry(self, eventid: int, entrytime: str):
        from .entry import Entry
        entry = Element("ENTRY", {"eventid": str(eventid), "entrytime": entrytime})
        self.element.find('ENTRIES').append(entry)
        self.enries.append(Entry(self.baseapi, entry, eventid, entrytime))

    def __eq__(self, value):
        return (
            isinstance(value, Athlete)
            and self.lastname.lower() == value.lastname.lower()
            and self.firstname.lower() == value.firstname.lower()
            and self.birthdate == value.birthdate
        )

    def __hash__(self):
        return sum(map(ord, (self.lastname + " " + self.firstname).lower()))
