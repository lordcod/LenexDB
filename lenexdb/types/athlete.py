from __future__ import annotations
from lxml.etree import Element
from typing import TYPE_CHECKING, Optional, Literal, List
from dataclasses import dataclass, field
from datetime import datetime
from ._base_obj import BaseObj, selfname
from ..utils import parse_bd

field()
if TYPE_CHECKING:
    from ..baseapi import BaseApi
    from .entry import Entry
    from .club import Club


@dataclass
class Athlete(BaseObj):
    baseapi: BaseApi
    element: Element
    club: Club
    lastname: str = field(metadata={"ext": selfname})
    firstname: str = field(metadata={"ext": selfname})
    birthdate: datetime | str  = field(metadata={"ext": selfname, "parse": lambda _, v: parse_bd(v)})
    gender: Literal["M", "F"] = field(metadata={"ext": selfname})
    athleteid: int
    license: Optional[str] = field(default=None, metadata={"ext": selfname})
    enries: List[Entry] = field(default=list)

    def add_entry(self, eventid: int, entrytime: str):
        from .entry import Entry

        entry = Element("ENTRY", {"eventid": str(eventid), "entrytime": entrytime})
        self.element.find("ENTRIES").append(entry)
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
