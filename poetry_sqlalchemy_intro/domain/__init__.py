from poetry_sqlalchemy_intro.common.base import create_tables

from .card import Card  # noqa: F401
from .chassis import Chassis  # noqa: F401
from .port import Port  # noqa: F401
from .router import Router  # noqa: F401

# TODO: automatic import of all ORM mapped classes from domain directory

create_tables()
