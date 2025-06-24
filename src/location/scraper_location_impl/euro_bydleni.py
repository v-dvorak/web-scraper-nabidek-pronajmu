from dataclasses import dataclass
from ..location_base import ScraperLocationImpl

@dataclass
class EuroBydleniLocationImpl(ScraperLocationImpl):
    input: str
    city: str
    lat: str
    lng: str
    south: str
    west: str
    north: str
    east: str

    @property
    def scraper_type(self):
        from ...scrapers import ScraperEuroBydleni
        return ScraperEuroBydleni
