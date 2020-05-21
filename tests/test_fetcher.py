import pytest
from systembolaget_openhours.fetcher import Fetcher
from .xmls import stores_christmas_xml


def test_parse_stores_from_xml(fetcher):
    assert len(fetcher.stores) == 11


def test_get_store_by_name(fetcher):
    store = fetcher.get_store_by_name("Norra Djurgårdsstaden")
    assert store.no == "0107"


def test_get_store_by_no(fetcher):
    store = fetcher.get_store_by_no("0113")
    assert store.name == "Sergel"


@pytest.fixture
def fetcher():
    fetcher = Fetcher()
    fetcher.parse_stores_from_xml(stores_christmas_xml)
    return fetcher
