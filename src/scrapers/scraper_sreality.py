import logging
from time import time
from urllib.parse import urljoin

import requests

from .rental_offer import RentalOffer
from .scraper_base import ScraperBase
from ..disposition import Disposition
from ..location import LocationBase, SrealityLocationImpl


class ScraperSreality(ScraperBase):
    name = "Sreality"
    logo_url = "https://www.sreality.cz/img/icons/android-chrome-192x192.png"
    color = 0xCC0000
    base_url = "https://www.sreality.cz"

    disposition_mapping = {
        Disposition.FLAT_1KK: "2",
        Disposition.FLAT_1: "3",
        Disposition.FLAT_2KK: "4",
        Disposition.FLAT_2: "5",
        Disposition.FLAT_3KK: "6",
        Disposition.FLAT_3: "7",
        Disposition.FLAT_4KK: "8",
        Disposition.FLAT_4: "9",
        Disposition.FLAT_5_UP: ("10", "11", "12"),
        Disposition.FLAT_OTHERS: "16",
    }

    _category_type_to_url = {
        0: "vse",
        1: "prodej",
        2: "pronajem",
        3: "drazby"
    }

    _category_main_to_url = {
        0: "vse",
        1: "byt",
        2: "dum",
        3: "pozemek",
        4: "komercni",
        5: "ostatni"
    }

    _category_sub_to_url = {
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
        12: "6-a-vice",
        16: "atypicky",
        47: "pokoj",
        37: "rodinny",
        39: "vila",
        43: "chalupa",
        33: "chata",
        35: "pamatka",
        40: "na-klic",
        44: "zemedelska-usedlost",
        19: "bydleni",
        18: "komercni",
        20: "pole",
        22: "louka",
        21: "les",
        46: "rybnik",
        48: "sady-vinice",
        23: "zahrada",
        24: "ostatni-pozemky",
        25: "kancelare",
        26: "sklad",
        27: "vyrobni-prostor",
        28: "obchodni-prostor",
        29: "ubytovani",
        30: "restaurace",
        31: "zemedelsky",
        38: "cinzovni-dum",
        49: "virtualni-kancelar",
        32: "ostatni-komercni-prostory",
        34: "garaz",
        52: "garazove-stani",
        50: "vinny-sklep",
        51: "pudni-prostor",
        53: "mobilni-domek",
        36: "jine-nemovitosti"
    }

    def __init__(self, dispositions: Disposition, location: LocationBase):
        super().__init__(dispositions)
        self._LOCATION_DATA: SrealityLocationImpl = location(self)

    def _create_link_to_offer(self, offer) -> str:
        return urljoin(self.base_url, "/detail" +
                       "/" + self._category_type_to_url[offer["seo"]["category_type_cb"]] +
                       "/" + self._category_main_to_url[offer["seo"]["category_main_cb"]] +
                       "/" + self._category_sub_to_url[offer["seo"]["category_sub_cb"]] +
                       "/" + offer["seo"]["locality"] +
                       "/" + str(offer["hash_id"]))

    def build_response(self) -> requests.Response | None:
        url = self.base_url + "/api/cs/v2/estates?category_main_cb=1&category_sub_cb="
        url += "|".join(self.get_dispositions_data())
        url += (f"&category_type_cb=2&locality_district_id={self._LOCATION_DATA.locality_district_id}"
                f"&locality_region_id={self._LOCATION_DATA.locality_region_id}&per_page=20")
        url += "&tms=" + str(int(time()))

        logging.debug("Sreality request: %s", url)

        return self.get_wrapper(url, headers=self.headers)

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response().json()

        try:
            items_data = response["_embedded"]["estates"]
            if not isinstance(items_data, list) or not items_data:
                logging.info(f"{self.name}: No offers found")
                return []
        except (TypeError, KeyError):
            logging.error(f"{self.name}: Unexpected response structure")
            return []

        items: list[RentalOffer] = []

        for item in items_data:
            # Ignorovat "tip" nabídky, které úplně neodpovídají filtrům a mění se s každým vyhledáváním
            if item["region_tip"] > 0:
                continue
            items.append(RentalOffer(
                scraper=self,
                link=self._create_link_to_offer(item),
                title=item["name"],
                location=item["locality"],
                price=item["price_czk"]["value_raw"],
                utilities=None,
                image_url=item["_links"]["image_middle2"][0]["href"]
            ))

        return items
