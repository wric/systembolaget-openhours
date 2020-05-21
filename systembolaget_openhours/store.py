from __future__ import annotations
from typing import List, OrderedDict, Tuple
from datetime import datetime
from statistics import mean
from .exception import DateOutOfRange
from .openhour import Openhour


class Store(object):
    def __init__(self, store: OrderedDict):
        self.type = store.get("Typ", "")
        self.no = store.get("Nr", "")
        self.name = store.get("Namn", "")
        self.address1 = store.get("Address1", "")
        self.address2 = store.get("Address2", "")
        self.address3 = store.get("Address3", "")
        self.address4 = store.get("Address4", "")
        self.address5 = store.get("Address5", "")
        self.telephone = store.get("Telefon", "")
        self.store_type = store.get("ButiksTyp", "")
        self.services = store.get("Tjanster", "")
        self.search_word = store.get("SokOrd", "")
        self.rt90x = store.get("RT90x", "")
        self.rt90y = store.get("RT90y", "")
        self.openhours = [
            Openhour(ot) for ot in store.get("Oppettider", "").split("_*")
        ]

    def is_datestring_deviating(self, date_string: str) -> Tuple[bool, str]:
        """ Required format 2020-05-21*. Does not handle timezones. """
        date = datetime.strptime(date_string[:10], "%Y-%m-%d")
        return self.is_date_deviating(date)

    def is_date_deviating(self, date: datetime) -> Tuple[bool, str]:
        openhour = self.get_openhour(date)
        return self.is_openhour_deviating(openhour)

    def is_openhour_deviating(self, openhour: Openhour) -> Tuple[bool, str]:
        deviating = (True, openhour.info)
        non_deviating = (False, openhour.info)

        if openhour.is_sunday():
            # Stores are always closed on Sundays.
            return non_deviating

        if openhour.is_closed():
            # Stores a usually open all days other than Sunday.
            return deviating

        if not openhour.is_weekday():
            # It's Saturday and not closed. Saturdays never deviates in open
            # hours unless closed.
            return non_deviating

        open_weekdays = [
            day
            for day in self.get_open_weekdays()
            if day.date != openhour.date
        ]

        mean_opens = mean(day.opens for day in open_weekdays)
        mean_closes = mean(day.closes for day in open_weekdays)

        # We're checking a weekday and assures that it opens
        # and closes as above the averega open and close time. If a week
        # day has limited open hours, it will should fulfill at least one of
        # these criterias.
        return (
            deviating
            if openhour.opens > mean_opens or openhour.closes < mean_closes
            else non_deviating
        )

    def get_all_evaluations(self) -> List[Tuple(bool, str)]:
        return [self.is_openhour_deviating(oh) for oh in self.openhours]

    def get_all_deviations(self) -> List[Tuple(bool, str)]:
        return [oh for oh in self.get_all_evaluations() if oh[0]]

    def get_openhour(self, date: datetime) -> Openhour:
        try:
            return next(oh for oh in self.openhours if oh.date == date)
        except StopIteration:
            raise DateOutOfRange("Date is not awailable.")

    def get_open_weekdays(self) -> List[Openhour]:
        return [
            oh
            for oh in self.openhours
            if oh.is_weekday() and not oh.is_closed()
        ]

    def number_of_deviations(self) -> int:
        return len(self.get_all_deviations())

    def has_deviation(self) -> bool:
        return self.number_of_deviations > 0
