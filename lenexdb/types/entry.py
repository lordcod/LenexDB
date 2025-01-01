from __future__ import annotations
from lxml.etree import Element
from typing import TYPE_CHECKING, Optional, Literal
from dataclasses import dataclass, field
from datetime import timedelta
from time import strftime, gmtime
from ._base_obj import BaseObj, selfname

timedelta()
if TYPE_CHECKING:
    from ..baseapi import BaseApi

def get_entrytime(entry, value) -> str:
    if isinstance(value, str):
        return value
    print(value, gmtime(value))
    return strftime('%H:%M:%S.%F', gmtime(value))

@dataclass
class Entry(BaseObj):
    baseapi: BaseApi
    element: Element
    eventid: int = field(metadata={"ext": selfname, "parse": lambda s, v: str(v)})
    entrytime: float | str = field(metadata={"ext": selfname, "parse": get_entrytime}) 