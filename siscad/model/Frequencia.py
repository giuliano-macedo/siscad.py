from collections import namedtuple
from datetime import datetime


class Frequencia(namedtuple("Frequencia", ["dt", "tipo", "chamadas"])):
    def _parser(year, day_month, hour_minute, tipo, chamadas):
        day, month = day_month.split("/")
        hour, minute = hour_minute.split(":")
        dt = datetime(
            year=int(year),
            day=int(day),
            month=int(month),
            hour=int(hour),
            minute=int(minute),
        )
        chamadas = [
            True if c == "P" else (False if c == "F" else None) for c in chamadas
        ]
        return Frequencia(dt, tipo, chamadas)
