from __future__ import annotations
from datetime import datetime
from lxml.etree import Element
from typing import TYPE_CHECKING, List
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..baseapi import BaseApi
    from .event import Event


@dataclass
class Session:
    baseapi: BaseApi
    element: Element
    dt: datetime
    name: str
    number: int
    events: List[Event]
