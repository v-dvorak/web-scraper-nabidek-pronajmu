from ..location_base import LocationBase, ScraperLocationImpl
from ..scraper_location_impl import *


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
                "49.195060",
                "16.606837",
                "49.109655",
                "16.428068",
                "49.294485",
                "16.727853",
            ),
            IdnesRealityLocationImpl("brno-mesto"),
            RealcityLocationImpl("brno-mesto-68"),
            RealingoLocationImpl("Brno"),
            RemaxLocationImpl("[116][3702]", False),
            SrealityLocationImpl("72", "14"),
            UlovDomovLocationImpl(
                "49.294485",
                "16.727853",
                "49.109655",
                "16.428068"
            )
        ]
