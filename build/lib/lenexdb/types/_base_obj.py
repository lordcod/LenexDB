from __future__ import annotations
from lxml.etree import ElementBase
from typing import TYPE_CHECKING, Any, Optional
import contextlib

if TYPE_CHECKING:
    from ..baseapi import BaseApi


class BaseObj:
    baseapi: BaseApi
    element: ElementBase

    def __post_init__(self) -> None:
        # print(fields(self))
        ...

    def ext(self, attribute_name: str) -> Optional[dict]:
        try:
            return self.__dataclass_fields__[attribute_name].metadata
        except Exception:
            return None

    def _setelement(self, name: str, value: Any):
        metadata = self.ext(name)
        if metadata is None:
            return

        if func := metadata.get("func"):
            with contextlib.suppress(Exception):
                return func(self, value)
            with contextlib.suppress(Exception):
                return func(value)
            return

        ext, parse = metadata.get("ext"), metadata.get("parse", lambda _, v: v)
        if not ext:
            return

        n = name if ext is selfname else ext
        if value is None:
            self.element.attrib.pop(n, None)
        else:
            self.element.set(n, parse(self, value))

    def __setattr__(self, name, value):
        self._setelement(name, value)
        super().__setattr__(name, value)


class SelfName:
    pass


selfname = SelfName()
