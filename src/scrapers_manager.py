import logging
import traceback

from .disposition import Disposition
from .location import PrahaLocation, BrnoLocation, LocationBase
from .scrapers import (RentalOffer, ScraperBase, ScraperBravis, ScraperEuroBydleni, ScraperIdnesReality,
                       ScraperRealcity, ScraperRealingo, ScraperRemax, ScraperSreality, ScraperUlovDomov,
                       ScraperBezrealitky)


def create_scrapers(dispositions: Disposition, location: LocationBase = None) -> list[ScraperBase]:
    if location is None:
        location = PrahaLocation()
    return [
        # Bravis is Brno based
        *([ScraperBravis(dispositions)] if isinstance(location, BrnoLocation) else []),
        ScraperEuroBydleni(dispositions, location),
        ScraperIdnesReality(dispositions, location),
        ScraperRealcity(dispositions, location),
        ScraperRealingo(dispositions, location),
        ScraperRemax(dispositions, location),
        ScraperSreality(dispositions, location),
        ScraperUlovDomov(dispositions, location),
        ScraperBezrealitky(dispositions, location),
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
