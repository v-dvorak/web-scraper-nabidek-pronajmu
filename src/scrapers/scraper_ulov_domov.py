import json
import logging

import requests

from .rental_offer import RentalOffer
from .scraper_base import ScraperBase
from ..disposition import Disposition
from ..location import LocationBase, UlovDomovLocationImpl
from ..utils import find_number_in_str


class ScraperUlovDomov(ScraperBase):
    name = "UlovDomov"
    logo_url = "https://www.ulovdomov.cz/favicon.png"
    color = 0xFFFFFF
    base_url = "https://www.ulovdomov.cz/fe-api/find/seperated-offers-within-bounds"

    disposition_mapping = {
        Disposition.FLAT_1KK: 2,
        Disposition.FLAT_1: 3,
        Disposition.FLAT_2KK: 4,
        Disposition.FLAT_2: 5,
        Disposition.FLAT_3KK: 6,
        Disposition.FLAT_3: 7,
        Disposition.FLAT_4KK: 8,
        Disposition.FLAT_4: 9,
        Disposition.FLAT_5_UP: (10, 11, 12, 13, 14, 15),  # 5kk, 5+1, 6kk, 6+1, 7kk, 7+1
        Disposition.FLAT_OTHERS: 16,
    }

    def __init__(self, dispositions: Disposition, location: LocationBase):
        super().__init__(dispositions)
        self._LOCATION_DATA: UlovDomovLocationImpl = location(self)

    def disposition_id_to_string(self, id) -> str:
        return {
            1: "garsonky",
            2: "1+kk",
            3: "1+1",
            4: "2+kk",
            5: "2+1",
            6: "3+kk",
            7: "3+1",
            8: "4+kk",
            9: "4+1",
            10: "5+kk",
            11: "5+1",
            12: "6+kk",
            13: "6+1",
            14: "7+kk",
            15: "7+1",
            16: "atypický",
            29: "domu",
            24: "spolubydlení (1 lůžkový)",
            25: "spolubydlení (2 lůžkový)",
            26: "spolubydlení (3 lůžkový)",
            27: "spolubydlení (4+ lůžkový)",
            28: "spolubydlení (samostatný pokoj)",
            "shared_room": "spolubydlení",
            "5_and_more": "5 a více"
        }.get(id, "")

    def build_response(self) -> requests.Response | None:
        json_request = {
            "acreage_from": "",
            "acreage_to": "",
            "added_before": "",
            "banner_panel_width_type": 480,
            "bounds": {
                "north_east": {
                    "lat": self._LOCATION_DATA.north_east_lat,
                    "lng": self._LOCATION_DATA.north_east_lng,
                },
                "south_west": {
                    "lat": self._LOCATION_DATA.south_west_lat,
                    "lng": self._LOCATION_DATA.south_west_lng,
                }
            },
            "conveniences": [],
            "dispositions": self.get_dispositions_data(),
            "furnishing": [],
            "is_price_commision_free": None,
            "limit": 20,
            "offer_type_id": None,
            "page": 1,
            "price_from": "",
            "price_to": "",
            "query": "",
            "sort_by": "date:desc",
            "sticker": None
        }

        logging.debug("UlovDomov request: %s", json.dumps(json_request))

        return self.post_wrapper(self.base_url, self.headers, json_request)

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response().json()

        try:
            items_data = response["offers"]
            if not isinstance(items_data, list) or not items_data:
                logging.info(f"{self.name}: No offers found")
                return []
        except (TypeError, KeyError):
            logging.error(f"{self.name}: Unexpected response structure")
            return []

        items: list[RentalOffer] = []
        for offer in items_data:
            items.append(RentalOffer(
                scraper=self,
                link=offer["absolute_url"],
                # TODO "Pronájem" podle ID?
                title="Pronájem " + self.disposition_id_to_string(offer["disposition_id"]) + " " + str(
                    offer["acreage"]) + " m²",
                location=offer["street"]["label"] + ", " + offer["village"]["label"] + " - " + offer["village_part"][
                    "label"],
                price=offer["price_rental"],
                utilities=find_number_in_str(offer["price_note"]),
                image_url=offer["photos"][0]["path"]
            ))
        return items
