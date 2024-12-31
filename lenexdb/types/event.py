from __future__ import annotations
from xml.etree.ElementTree import Element
from typing import TYPE_CHECKING, Optional, Literal
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..baseapi import BaseApi

@dataclass
class Event:
    baseapi: BaseApi
    element: Element
    eventid: int
    gender: Literal['M', 'F']
    number: int
    order: int
    round: str
    preevent: int
    swim_style: SwimStyle

@dataclass
class SwimStyle:
    element: Element
    distance: int
    relaycount: int
    stroke: str