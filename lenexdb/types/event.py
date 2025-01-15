from __future__ import annotations
from lxml.etree import Element
from typing import TYPE_CHECKING, Optional, Literal, List
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..baseapi import BaseApi


@dataclass
class Event:
    baseapi: BaseApi
    element: Element
    eventid: int
    gender: Literal["M", "F", "X"]
    number: int
    order: int
    round: str
    preevent: int
    swim_style: SwimStyle
    agegroups: List[AgeGroup]
    timestandardrefs: List[TimeStandardRef]


@dataclass
class SwimStyle:
    element: Element
    distance: int
    relaycount: int
    stroke: str


@dataclass
class TimeStandardRef:
    element: Element
    marker: str
    timestandardlistid: int


@dataclass
class AgeGroup:
    element: Element
    agegroupid: int
    agemax: int
    agemin: int
