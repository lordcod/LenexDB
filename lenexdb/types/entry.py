from __future__ import annotations
from xml.etree.ElementTree import Element
from typing import TYPE_CHECKING, Optional, Literal
from dataclasses import dataclass
from datetime import timedelta
from time import strftime, gmtime

timedelta()
if TYPE_CHECKING:
    from ..baseapi import BaseApi

@dataclass
class Entry:
    baseapi: BaseApi
    element: Element
    eventid: int
    entrytime: float
    
    def get_entrytime(self) -> str:
        return strftime('%H:%M:%S.%f', gmtime(self.entrytime))