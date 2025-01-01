from __future__ import annotations
from lxml.etree import Element
from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from ._base_obj import BaseObj, selfname

if TYPE_CHECKING:
    from ..baseapi import BaseApi


def get_entrytime(_, value) -> str:
    if isinstance(value, str):
        return value
    r = datetime.fromtimestamp(value).strftime('%H:%M:%S.%f')
    return r[:-4]


@dataclass
class Entry(BaseObj):
    baseapi: BaseApi
    element: Element
    eventid: int = field(
        metadata={"ext": selfname, "parse": lambda s, v: str(v)})
    entrytime: float | str = field(
        metadata={"ext": selfname, "parse": get_entrytime})
