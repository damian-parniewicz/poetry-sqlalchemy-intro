from sqlalchemy import Column, ForeignKey, Integer, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from ..common.base import Base
from .card import Card


class Chassis(Base):
    __tablename__ = "chassis"

    id = Column(Integer, primary_key=True)
    max_slots = Column(Integer)

    router_id = Column(Integer, ForeignKey("router.id"))
    router = relationship("Router", back_populates="chassis")

    cards = relationship("Card", back_populates="chassis")

    def __repr__(self) -> str:
        return (
            f"Chassis(id={self.id!r}, max_slots={self.max_slots!r}, "
            f"router_id={self.router_id!r}))"
        )

    @hybrid_property
    def active_port_count(self) -> int:
        return sum(card.active_port_count for card in self.cards)

    @active_port_count.expression  # type:ignore[no-redef]
    def active_port_count(cls) -> int:
        return (
            select(func.sum(Card.active_port_count))
            .where(Card.chassis_id == cls.id)
            .label("active_port_count")
        )
