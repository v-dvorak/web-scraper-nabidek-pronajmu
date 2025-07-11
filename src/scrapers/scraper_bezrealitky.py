""" Scraper for BezRealitky.cz
author: Mark Barzali
"""

import json
import logging
from abc import ABC as abstract
from typing import ClassVar

import requests

from ..disposition import Disposition
from ..location import LocationBase
from ..scrapers import ScraperBase, RentalOffer


class ScraperBezrealitky(ScraperBase):
    name = "BezRealitky"
    logo_url = "https://www.bezrealitky.cz/favicon.png"
    color = 0x00CC00
    base_url = "https://www.bezrealitky.cz"
    file: ClassVar[str] = "./graphql/bezrealitky.json"

    API: ClassVar[str] = "https://api.bezrealitky.cz/"
    OFFER_TYPE: ClassVar[str] = "PRONAJEM"
    ESTATE_TYPE: ClassVar[str] = "BYT"

    class Routes(abstract):
        GRAPHQL: ClassVar[str] = "graphql/"
        OFFERS: ClassVar[str] = "nemovitosti-byty-domy/"

    disposition_mapping = {
        Disposition.FLAT_1KK: "DISP_1_KK",
        Disposition.FLAT_1: "DISP_1_1",
        Disposition.FLAT_2KK: "DISP_2_KK",
        Disposition.FLAT_2: "DISP_2_1",
        Disposition.FLAT_3KK: "DISP_3_KK",
        Disposition.FLAT_3: "DISP_3_1",
        Disposition.FLAT_4KK: "DISP_4_KK",
        Disposition.FLAT_4: "DISP_4_1",
        Disposition.FLAT_5_UP: None,
        Disposition.FLAT_OTHERS: None,
    }

    def __init__(self, disposition: Disposition, location: LocationBase):
        super().__init__(disposition)
        self._LOCATION_ID: str = location(self).location_id
        self._read_config()
        self._patch_config()

    def _read_config(self) -> None:
        with open(ScraperBezrealitky.file, "r") as file:
            self._config = json.load(file)

    def _patch_config(self):
        match = {
            "estateType": self.ESTATE_TYPE,
            "offerType": self.OFFER_TYPE,
            "disposition": self.get_dispositions_data(),
            "regionOsmIds": [self._LOCATION_ID],
        }
        self._config["variables"].update(match)

    @staticmethod
    def _create_link_to_offer(item: dict) -> str:
        return f"{ScraperBezrealitky.base_url}/{ScraperBezrealitky.Routes.OFFERS}{item}"

    def build_response(self) -> requests.Response:
        return self.post_wrapper(
            url=f"{ScraperBezrealitky.API}{ScraperBezrealitky.Routes.GRAPHQL}",
            json=self._config
        )

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response().json()

        try:
            items_data = response["data"]["listAdverts"]["list"]
            if not isinstance(items_data, list) or not items_data:
                logging.info(f"{self.name}: No offers found")
                return []
        except (TypeError, KeyError):
            logging.error(f"{self.name}: Unexpected response structure")
            return []

        items: list[RentalOffer] = []

        for item in items_data:
            items.append(
                RentalOffer(
                    scraper=self,
                    link=self._create_link_to_offer(item["uri"]),
                    title=item["imageAltText"],
                    location=item["address"],
                    price=item["price"],
                    utilities=item["charges"],
                    image_url=item["mainImage"]["url"] if item["mainImage"] else "",
                )
            )
        return items
