import pytest
from systembolaget_openhours.openhour import Openhour


MONDAY = "2019-12-23;10:00;19:00;;;0;"
SATURDAY = "2019-12-28;10:00;15:00;;;0;"
SUNDAY = "2019-12-22;00:00;00:00;;;-;"
CHRISTMAS_EVE = "2019-12-24;00:00;00:00;;;Julafton;"


@pytest.mark.parametrize(
    "openhour_text,expected",
    [
        (MONDAY, False),
        (SATURDAY, False),
        (SUNDAY, True),
        (CHRISTMAS_EVE, False),
    ],
)
def test_sunday_is_sunday(openhour_text, expected):
    openhour = Openhour(openhour_text)
    assert openhour.is_sunday() is expected


@pytest.mark.parametrize(
    "openhour_text,expected",
    [
        (MONDAY, False),
        (SATURDAY, False),
        (SUNDAY, True),
        (CHRISTMAS_EVE, True),
    ],
)
def test_is_closed(openhour_text, expected):
    openhour = Openhour(openhour_text)
    assert openhour.is_closed() is expected


@pytest.mark.parametrize(
    "openhour_text,expected",
    [
        (MONDAY, True),
        (SATURDAY, False),
        (SUNDAY, False),
        (CHRISTMAS_EVE, True),
    ],
)
def test_is_weekday(openhour_text, expected):
    openhour = Openhour(openhour_text)
    assert openhour.is_weekday() is expected
