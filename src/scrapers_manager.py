import logging
import traceback

from .location import BrnoLocation
from .disposition import Disposition
from .scrapers import (RentalOffer, ScraperBase, ScraperBravis, ScraperEuroBydleni, ScraperIdnesReality,
                       ScraperRealcity, ScraperRealingo, ScraperRemax, ScraperSreality, ScraperUlovDomov,
                       ScraperBezrealitky)


def create_scrapers(dispositions: Disposition) -> list[ScraperBase]:
    location = None
    return [
        # Bravis is Brno based
        *([ScraperBravis(dispositions)] if isinstance(location, BrnoLocation) else []),
        ScraperEuroBydleni(dispositions, BrnoLocation()),
        ScraperIdnesReality(dispositions),
        ScraperRealcity(dispositions),
        ScraperRealingo(dispositions),
        ScraperRemax(dispositions),
        ScraperSreality(dispositions),
        ScraperUlovDomov(dispositions),
        ScraperBezrealitky(dispositions, BrnoLocation()),
    ]


def fetch_latest_offers(scrapers: list[ScraperBase]) -> list[RentalOffer]:
    """Získá všechny nejnovější nabídky z dostupných serverů

    Returns:
        list[RentalOffer]: Seznam nabídek
    """

    offers: list[RentalOffer] = []
    for scraper in scrapers:
        try:
            for offer in scraper.get_latest_offers():
                offers.append(offer)
        except Exception:
            logging.error(traceback.format_exc())

    return offers
