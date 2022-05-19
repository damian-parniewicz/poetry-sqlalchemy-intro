import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from ..common.base import Base


class EthernetSpeed(enum.Enum):
    Ethernet_1G = "Ethernet_1G"
    Ethernet_10G = "Ethernet_10G"
    Ethernet_25G = "Ethernet_25G"
    Ethernet_40G = "Ethernet_40G"
    Ethernet_100G = "Ethernet_100G"
    Ethernet_400G = "Ethernet_400G"


class State(enum.Enum):
    UP = "UP"
    DOWN = "DOWN"


class Port(Base):
    __tablename__ = "port"

    id = Column(Integer, primary_key=True)
    speed = Column(Enum(EthernetSpeed))
    state = Column(Enum(State), default=State.UP)

    card_id = Column(Integer, ForeignKey("card.id"))
    card = relationship("Card", back_populates="ports")

    def __repr__(self) -> str:
        return (
            f"Port(id={self.id!r}, speed={self.speed!r}, "
            f"card_id={self.card_id!r})"
        )

    @hybrid_property
    def is_up(self) -> bool:
        return self.state == State.UP
