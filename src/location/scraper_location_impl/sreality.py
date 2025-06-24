from dataclasses import dataclass

from ..location_base import ScraperLocationImpl


@dataclass(frozen=True)
class SrealityLocationImpl(ScraperLocationImpl):
    locality_district_id: str
    locality_region_id: str

    @property
    def scraper_type(self):
        from ...scrapers.impl import ScraperSreality
        return ScraperSreality
