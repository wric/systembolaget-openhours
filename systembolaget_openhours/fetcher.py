from __future__ import annotations
import requests
import xmltodict
from typing import List
from .store import Store


URL = "https://www.systembolaget.se/api/assortment/stores/xml"


class Fetcher(object):
    def __init__(self, url: str = URL, stores: List[Store] = None):
        self.url = url
        self.stores = stores

    def get_stores(self):
        if not self.stores:
            self.fetch_stores()
        return self.stores

    def fetch_stores(self):
        res = requests.get(self.url)
        res.raise_for_status()
        self.parse_stores_from_xml(res.text)

    def parse_stores_from_xml(self, text: str):
        xml = xmltodict.parse(text)
        stores = xml.get("ButikerOmbud").get("ButikOmbud")
        self.stores = [
            Store(store) for store in stores if store["Typ"] == "Butik"
        ]

    def get_store_by_name(self, name: str) -> Store:
        return next(
            (store for store in self.get_stores() if store.name == name), None
        )

    def get_store_by_no(self, no: str) -> Store:
        return next(
            (store for store in self.get_stores() if store.no == no), None
        )
