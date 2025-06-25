import logging
from abc import abstractmethod
from typing import Any

import requests
from requests import Response
from requests.exceptions import RequestException

from .rental_offer import RentalOffer
from ..disposition import Disposition
from ..utils import flatten


class ScraperBase():
    """Hlavní třída pro získávání aktuálních nabídek pronájmu bytů z různých služeb
    """

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    headers = {"User-Agent": user_agent}

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def logo_url(self) -> str:
        pass

    @property
    @abstractmethod
    def color(self) -> int:
        pass

    @property
    @abstractmethod
    def disposition_mapping(self) -> dict[Disposition, Any]:
        pass

    def __init__(self, disposition: Disposition) -> None:
        self.disposition = disposition

    def get_dispositions_data(self) -> list:
        return list(flatten([self.disposition_mapping[d] for d in self.disposition]))

    @abstractmethod
    def build_response(self) -> Response | None:
        """Vytvoří a pošle dotaz na server pro získání nabídek podle nakonfigurovaných parametrů

        Raises:
            NotImplementedError: Pokud potomek neimplementuje tuto metodu

        Returns:
            Response: Odpověď nabídkového serveru obsahující neparsované nabídky
        """
        raise NotImplementedError("Server request builder is not implemeneted")

    @abstractmethod
    def get_latest_offers(self) -> list[RentalOffer]:
        """Načte a vrátí seznam nejnovějších nabídek bytů k pronájmu z dané služby

        Raises:
            NotImplementedError: Pokud potomek neimplementuje tuto metodu

        Returns:
            list[RentalOffer]: Seznam nabízených bytů k pronájmu
        """
        raise NotImplementedError("Fetching new results is not implemeneted")

    def post_wrapper(self,
                     url: str,
                     headers: dict[str, str] = None,
                     json: dict[str, Any] = None,
                     cookies: dict[str, str] = None,
                     data: dict[str, Any] = None,
                     ) -> Response | None:
        try:
            response = requests.post(url, headers=headers, json=json, cookies=cookies, data=data)
            response.raise_for_status()
            return response
        except RequestException as e:
            logging.error(f"{self.name}: Request to {url} failed: {str(e)}")
            return None

    def get_wrapper(self, url: str, headers: dict[str, Any]) -> Response | None:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except RequestException as e:
            logging.error(f"{self.name}: Request to {url} failed: {str(e)}")
            return None
