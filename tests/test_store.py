import pytest
import xmltodict
from datetime import datetime
from systembolaget_openhours.store import Store
from systembolaget_openhours.exception import DateOutOfRange
from .xmls import backaplan_christmas_xml, backaplan_easter_xml


def test_parse_store(backaplan_christmas):
    store = Store(backaplan_christmas)
    assert store.name == "Backaplan"


def test_parse_openhours(backaplan_christmas):
    store = Store(backaplan_christmas)
    assert len(store.openhours) == 16


def test_get_openhour(backaplan_christmas):
    store = Store(backaplan_christmas)
    date = datetime(2019, 12, 23)
    openhour = store.get_openhour(date)
    assert openhour.date == date


def test_get_openhour_not_in_range(backaplan_christmas):
    store = Store(backaplan_christmas)
    date = datetime(2020, 12, 23)
    with pytest.raises(DateOutOfRange):
        store.get_openhour(date)


def test_is_openhour_deviating_regular_saturday(backaplan_christmas):
    """ Saturdays has different open hours. """
    store = Store(backaplan_christmas)
    date = datetime(2019, 12, 28)
    is_deviating, info = store.is_date_deviating(date)
    assert is_deviating is False
    assert info == "0"


def test_is_openhour_deviating_sunday(backaplan_christmas):
    store = Store(backaplan_christmas)
    date = datetime(2019, 12, 22)
    is_deviating, info = store.is_date_deviating(date)
    assert is_deviating is False
    assert info == "-"


def test_is_openhour_deviating_christmas_eve(backaplan_christmas):
    store = Store(backaplan_christmas)
    date = datetime(2019, 12, 24)
    is_deviating, info = store.is_date_deviating(date)
    assert is_deviating is True
    assert info == "Julafton"


def test_is_openhour_deviating_new_years_eve(backaplan_christmas):
    """ New years eve is a special case. 2019 it was a Tuesday, but it has the
        open hours of a Saturday. However, not all days before holiday days
        follows this pattern (e.g. 2020-04-09, the day before "Långfredag").
    """
    store = Store(backaplan_christmas)
    date = datetime(2019, 12, 31)
    is_deviating, info = store.is_date_deviating(date)
    assert is_deviating is True
    assert info == "0"


def test_is_openhour_deviating_day_before_langfredag(backaplan_easter):
    """ Assert that we don't assume that day before holiday is deviant. """
    store = Store(backaplan_easter)
    date = datetime(2020, 4, 9)
    is_deviating, info = store.is_date_deviating(date)
    assert is_deviating is False
    assert info == "0"


def test_has_deviation(backaplan_christmas):
    store = Store(backaplan_christmas)
    assert store.has_deviation() is True


def test_backaplan_easter(backaplan_easter):
    store = Store(backaplan_easter)
    evaluations = store.get_all_evaluations()
    expected = [
        (False, "0"),
        (True, "Långfredag"),
        (False, "0"),
        (False, "-"),
        (True, "Annandag påsk"),
        (False, "0"),
        (False, "0"),
        (False, "0"),
        (False, "0"),
        (False, "0"),
        (False, "-"),
        (False, "0"),
        (False, "0"),
        (False, "0"),
        (False, "0"),
        (False, "0"),
    ]
    assert evaluations == expected


def test_backaplan_christmas(backaplan_christmas):
    store = Store(backaplan_christmas)
    evaluations = store.get_all_evaluations()
    expected = [
        (False, "-"),
        (False, "0"),
        (True, "Julafton"),
        (True, "Juldagen"),
        (True, "Annandag jul"),
        (False, "0"),
        (False, "0"),
        (False, "-"),
        (False, "0"),
        (True, "0"),
        (True, "Nyårsdagen"),
        (False, "0"),
        (False, "0"),
        (False, "0"),
        (False, "-"),
        (True, "Trettondag jul"),
    ]
    assert evaluations == expected


@pytest.fixture
def backaplan_christmas():
    return xmltodict.parse(backaplan_christmas_xml).get("ButikOmbud")


@pytest.fixture
def backaplan_easter():
    return xmltodict.parse(backaplan_easter_xml).get("ButikOmbud")
