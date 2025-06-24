from dataclasses import dataclass

from ..location_base import ScraperLocationImpl

# TODO: FIXME: Test Realingo further, website is down at the moment.
@dataclass(frozen=True)
class RealingoLocationImpl(ScraperLocationImpl):
    location_name: str

    @property
    def scraper_type(self):
        from ...scrapers import ScraperRealingo
        return ScraperRealingo
