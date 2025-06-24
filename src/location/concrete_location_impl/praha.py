from ..location_base import LocationBase, ScraperLocationImpl
from ..scraper_location_impl import BezrealitkyLocationImpl, EuroBydleniLocationImpl


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
                "50.0775891",
                "14.4313489",
                "49.9935871",
                "14.2830505",
                "50.1411559",
                "14.6167603"
            )
        ]
