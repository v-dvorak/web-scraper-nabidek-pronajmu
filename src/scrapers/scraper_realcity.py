import logging
import re

import requests
from bs4 import BeautifulSoup

from .rental_offer import RentalOffer
from .scraper_base import ScraperBase
from ..disposition import Disposition
from ..location import LocationBase


class ScraperRealcity(ScraperBase):
    name = "REALCITY"
    logo_url = "https://files.janchaloupka.cz/realcity.png"
    color = 0xB60D1C

    disposition_mapping = {
        Disposition.FLAT_1KK: "%221%2Bkk%22",
        Disposition.FLAT_1: "%221%2B1%22",
        Disposition.FLAT_2KK: "%222%2Bkk%22",
        Disposition.FLAT_2: "%222%2B1%22",
        Disposition.FLAT_3KK: "%223%2Bkk%22",
        Disposition.FLAT_3: "%223%2B1%22",
        Disposition.FLAT_4KK: "%224%2Bkk%22",
        Disposition.FLAT_4: ("%224%2B1%22", "%224%2B2%22"),  # 4+1, 4+2
        Disposition.FLAT_5_UP: (
        "%225%2Bkk%22", "%225%2B1%22", "%225%2B2%22", "%226%2Bkk%22", "%226%2B1%22", "%22disp_more%22"),
        # 5kk, 5+1, 5+2, 6kk, 6+1, ++
        Disposition.FLAT_OTHERS: ("%22atyp%22", "%22disp_nospec%22"),  # atyp, unknown
    }

    def __init__(self, dispositions: Disposition, location: LocationBase):
        super().__init__(dispositions)
        self._LOCATION_ID: str = location(self).location_id

    def build_response(self) -> requests.Response:
        url = f"https://www.realcity.cz/pronajem-bytu/{self._LOCATION_ID}?sp=%7B%22locality%22%3A%5B{self._LOCATION_ID.split('-')[-1]}%5D%2C%22transactionTypes%22%3A%5B%22rent%22%5D%2C%22propertyTypes%22%3A%5B%7B%22propertyType%22%3A%22flat%22%2C%22options%22%3A%7B%22disposition%22%3A%5B"
        url += "%2C".join(self.get_dispositions_data())
        url += "%5D%7D%7D%5D%7D"

        logging.debug("REALCITY request: %s", url)

        return self.get_wrapper(url, headers=self.headers)

    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response()

        if response is None:
            logging.info(f"{self.name}: No offers found")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        items: list[RentalOffer] = []

        for item in soup.select("#rc-advertise-result .media.advertise.item"):
            image = item.find("div", "pull-left image")
            body = item.find("div", "media-body")
            items.append(RentalOffer(
                scraper=self,
                link="https://www.realcity.cz" + body.find("div", "title").a.get("href"),
                title=body.find("div", "title").a.get_text() or "Chybí titulek",
                location=body.find("div", "address").get_text().strip() or "Chybí adresa",
                price=int(re.sub(r'\D+', '', body.find("div", "price").get_text() or "0")),
                utilities=None,
                image_url="https:" + image.img.get("src")
            ))

        return items
