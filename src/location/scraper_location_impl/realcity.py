from dataclasses import dataclass

from ..location_base import ScraperLocationImpl


@dataclass(frozen=True)
class RealcityLocationImpl(ScraperLocationImpl):
    location_id: str

    @property
    def scraper_type(self):
        from ...scrapers import ScraperRealcity
        return ScraperRealcity
