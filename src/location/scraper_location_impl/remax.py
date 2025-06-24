from dataclasses import dataclass

from ..location_base import ScraperLocationImpl


@dataclass(frozen=True)
class RemaxLocationImpl(ScraperLocationImpl):
    location_id: str
    is_region: bool

    @property
    def scraper_type(self):
        from ...scrapers.impl import ScraperRemax
        return ScraperRemax
