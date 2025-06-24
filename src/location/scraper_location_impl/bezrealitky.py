from dataclasses import dataclass

from ..location_base import ScraperLocationImpl


@dataclass(frozen=True)
class BezrealitkyLocationImpl(ScraperLocationImpl):
    location_id: str

    @property
    def scraper_type(self):
        from ...scrapers.impl import ScraperBezrealitky
        return ScraperBezrealitky
