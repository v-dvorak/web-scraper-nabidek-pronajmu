from dataclasses import dataclass

from ..location_base import ScraperLocationImpl


@dataclass
class UlovDomovLocationImpl(ScraperLocationImpl):
    north_east_lat: str
    north_east_lng: str
    south_west_lat: str
    south_west_lng: str

    @property
    def scraper_type(self):
        from ...scrapers import ScraperUlovDomov
        return ScraperUlovDomov
