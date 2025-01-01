from typing import Optional
from datetime import datetime as dt


def parse_dt(date: str, daytime: Optional[str] = None) -> dt:
    if daytime is None:
        return dt.strptime(date, "%Y-%m-%d")
    return dt.strptime(f"{date} {daytime}", "%Y-%m-%d %H:%M")


def parse_time(t: str) -> float:
    hours, minutes, sm = t.split(":")
    return int(hours) * 60 * 60 + int(minutes) * 60 + float(sm)


def parse_bd(v) -> str:
    return v.strftime("%Y-%m-%d") if isinstance(v, dt) else v


if __name__ == "__main__":
    t = parse_time("00:11:33.31")
    print(t)
