from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .chassis import Chassis  # noqa: F401

from sqlalchemy import Column, ForeignKey, Integer, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from ..common.base import Base
from .port import Port, State


class Card(Base):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True)
    max_ports = Column(Integer)

    chassis_id = Column(Integer, ForeignKey("chassis.id"))
    chassis = relationship("Chassis", back_populates="cards")

    ports = relationship("Port", back_populates="card")

    def __repr__(self) -> str:
        return (
            f"Card(id={self.id!r}, max_ports={self.max_ports!r}, "
            f" chassis_id={self.chassis_id!r}))"
        )

    @hybrid_property
    def active_port_count(self) -> int:
        return sum(1 for port in self.ports if port.is_up)

    @active_port_count.expression  # type:ignore[no-redef]
    def active_port_count(cls) -> int:
        return (
            select(func.count(Port))
            .where(Port.is_up == State.UP)
            .label("active_port_count")
        )
