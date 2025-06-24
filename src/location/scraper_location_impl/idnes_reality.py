from dataclasses import dataclass

from ..location_base import ScraperLocationImpl


@dataclass
class IdnesRealityLocationImpl(ScraperLocationImpl):
    location_name: str

    @property
    def scraper_type(self):
        from ...scrapers.impl import ScraperIdnesReality
        return ScraperIdnesReality
