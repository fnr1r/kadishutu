from datetime import datetime, timedelta


def unreal_to_python_datetime(ticks: int) -> datetime:
    return datetime.min + timedelta(microseconds=ticks/10)


def python_to_unreal_datetime(time: datetime) -> int:
    return int((time - datetime.min).total_seconds() * (10 ** 7))
