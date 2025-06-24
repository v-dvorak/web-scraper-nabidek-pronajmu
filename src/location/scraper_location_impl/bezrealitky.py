from ..location_base import ScraperLocationImpl
from dataclasses import dataclass

@dataclass(frozen=True)
class BezrealitkyLocationImpl(ScraperLocationImpl):
    location_id: str

    @property
    def scraper_type(self):
        from ...scrapers import ScraperBezrealitky
        return ScraperBezrealitky
