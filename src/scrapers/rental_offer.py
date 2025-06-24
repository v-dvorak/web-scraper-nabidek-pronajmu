import re
from dataclasses import dataclass

DEFAULT_PROPERTY_VALUE = "Neuvedeno ❓"


@dataclass
class RentalOffer:
    """Nabídka pronájmu bytu"""

    link: str
    """URL adresa na nabídku"""

    title: str
    """Popis nabídky (nejčastěji počet pokojů, výměra)"""

    location: str
    """Lokace bytu (městská část, ulice)"""

    price: int
    """Cena pronájmu za měsíc bez poplatků a energií"""

    utilities: int | None
    """Cena poplatků a energií"""

    image_url: str
    """Náhledový obrázek nabídky"""

    scraper: "ScraperBase"
    """Odkaz na instanci srapera, ze kterého tato nabídka pochází"""

    _disposition_match = re.compile(r"(\d\s*\+\s*(?:kk|\d)|\d\s*kk)", re.IGNORECASE)
    _size_match = re.compile(r"(\d+(?:\s*[.,]\s*\d+)?)\s*(?:m2|m²)", re.IGNORECASE)

    @property
    def total_price(self) -> int:
        return self.price + self.utilities if self.utilities is not None else self.price

    @property
    def true_utilities(self) -> str | int:
        return self.utilities if self.utilities is not None else DEFAULT_PROPERTY_VALUE

    @property
    def disposition(self) -> str:
        match = self._disposition_match.search(self.title)
        return match.group(1) if match is not None else DEFAULT_PROPERTY_VALUE

    @property
    def clean_title(self) -> str:
        return self.title.strip().replace(" ,", ",")

    @property
    def size(self) -> str:
        match = self._size_match.search(self.title)
        if match is None:
            return DEFAULT_PROPERTY_VALUE

        number = match.group(1)
        number = re.sub(r"\s+", "", number)
        number = number.replace(".", ",")
        return number
