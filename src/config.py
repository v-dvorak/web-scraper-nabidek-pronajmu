import functools
import operator
import os
from pathlib import Path

import environ
from dotenv import load_dotenv

from .disposition import Disposition
from .location import LocationBase

load_dotenv(".env")

app_env = os.getenv("APP_ENV")
if app_env:
    load_dotenv(".env." + app_env, override=True)

load_dotenv(".env.local", override=True)

_str_to_disposition_map = {
    "1+kk": Disposition.FLAT_1KK,
    "1+1": Disposition.FLAT_1,
    "2+kk": Disposition.FLAT_2KK,
    "2+1": Disposition.FLAT_2,
    "3+kk": Disposition.FLAT_3KK,
    "3+1": Disposition.FLAT_3,
    "4+kk": Disposition.FLAT_4KK,
    "4+1": Disposition.FLAT_4,
    "5++": Disposition.FLAT_5_UP,
    "others": Disposition.FLAT_OTHERS
}


def dispositions_converter(raw_disps: str):
    return functools.reduce(operator.or_, map(lambda d: _str_to_disposition_map[d], raw_disps.split(",")),
                            Disposition.NONE)


def locations_converter(raw_location: str) -> LocationBase:
    raw_location = raw_location.strip().lower()
    for subc in LocationBase.__subclasses__():
        if raw_location == subc.__name__.replace("Location", "").lower():
            return subc()
    raise ValueError(f"Location '{raw_location}' is not valid")


@environ.config(prefix="")
class Config:
    debug: bool = environ.bool_var()
    found_offers_file: Path = environ.var(converter=Path)
    refresh_interval_daytime_minutes: int = environ.var(converter=int)
    refresh_interval_nighttime_minutes: int = environ.var(converter=int)
    dispositions: Disposition = environ.var(converter=dispositions_converter)
    maximal_rent_value: int = environ.var(converter=int)
    location: LocationBase = environ.var(converter=locations_converter)

    @environ.config()
    class Discord:
        token = environ.var()
        offers_channel = environ.var(converter=int)
        dev_channel = environ.var(converter=int)

    discord: Discord = environ.group(Discord)


config: Config = Config.from_environ()
