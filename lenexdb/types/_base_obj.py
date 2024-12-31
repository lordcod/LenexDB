from __future__ import annotations
from xml.etree.ElementTree import Element
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..baseapi import BaseApi

class BaseObj:
    baseapi: BaseApi
    element: Element
