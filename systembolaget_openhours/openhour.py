from datetime import datetime


SATURDAY = 5
SUNDAY = 6


class Openhour(object):
    def __init__(self, openhour):
        info = openhour.split(";")
        date = datetime(*[int(i) for i in info[0].split("-")])
        self.date = date
        self.opens = float(info[1].replace(":", "."))
        self.closes = float(info[2].replace(":", "."))
        self.info = info[-2]

    def is_sunday(self):
        return self.date.weekday() == SUNDAY

    def is_closed(self):
        return self.opens == 0 and self.closes == 0

    def is_weekday(self):
        return self.date.weekday() < SATURDAY
