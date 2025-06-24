""" Scraper for BezRealitky.cz
author: Mark Barzali
"""

import json
from abc import ABC as abstract
from typing import ClassVar

from ..disposition import Disposition
from ..scrapers import ScraperBase, RentalOffer
from ..location import LocationBase
import requests


class ScraperBezrealitky(ScraperBase):

    name = "BezRealitky"
    logo_url = "https://www.bezrealitky.cz/manifest-icon-192.maskable.png"
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
        return requests.post(
            url=f"{ScraperBezrealitky.API}{ScraperBezrealitky.Routes.GRAPHQL}",
            json=self._config
        )

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response().json()

        return [  # type: list[RentalOffer]
            RentalOffer(
                scraper=self,
                link=self._create_link_to_offer(item["uri"]),
                title=item["imageAltText"],
                location=item["address"],
                price=f"{item['price']} / {item['charges']}",
                image_url=item["mainImage"]["url"] if item["mainImage"] else "",
            )
            for item in response["data"]["listAdverts"]["list"]
        ]
