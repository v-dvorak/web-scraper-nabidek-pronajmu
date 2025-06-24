from ..location_base import LocationBase, ScraperLocationImpl
from ..scraper_location_impl import *


class PrahaLocation(LocationBase):
    @property
    def name(self) -> str:
        return "Praha"

    @property
    def _location_impls(self) -> list[ScraperLocationImpl]:
        return [
            BezrealitkyLocationImpl("R435514"),
            EuroBydleniLocationImpl(
                "Praha, Česko",
                "Praha, Česko",
                "50.077589",
                "14.431349",
                "49.993587",
                "14.283051",
                "50.141156",
                "14.616760"
            ),
            IdnesRealityLocationImpl("praha"),
            RealcityLocationImpl("praha-2604"),
            RealingoLocationImpl("Praha"),
            RemaxLocationImpl("praha", True),
            SrealityLocationImpl("0", "10"),
            UlovDomovLocationImpl(
                "50.141156",
                "14.616760",
                "49.993587",
                "14.283051",
            )
        ]
