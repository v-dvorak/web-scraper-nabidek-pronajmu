from abc import abstractmethod, ABC
from typing import Self

from ..scrapers import ScraperBase

class ScraperLocationImpl(ABC):
    @property
    @abstractmethod
    def scraper_type(self):
        pass


class LocationBase(ABC):
    @property
    @abstractmethod
    def _location_impls(self) -> list[ScraperLocationImpl]:
        pass

    def __call__(self, scraper_instance: ScraperBase) -> Self:
        for location in self._location_impls:
            if isinstance(scraper_instance, location.scraper_type):
                return location

    @property
    @abstractmethod
    def name(self) -> str:
        pass

