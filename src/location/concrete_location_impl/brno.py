from ..location_base import LocationBase, ScraperLocationImpl
from ..scraper_location_impl import BezrealitkyLocationImpl, EuroBydleniLocationImpl


class BrnoLocation(LocationBase):
    @property
    def name(self) -> str:
        return "Brno"

    @property
    def _location_impls(self) -> list[ScraperLocationImpl]:
        return [
            BezrealitkyLocationImpl("R438171"),
            EuroBydleniLocationImpl(
                "Brno, Česko",
                "Brno, Česko",
                "49.1950602",
                "16.6068371",
                "49.10965517428777",
                "16.42806782678905",
                "49.294484956308",
                "16.72785321479357",
            )
        ]
