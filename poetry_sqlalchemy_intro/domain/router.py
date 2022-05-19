from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from ..common.base import Base
from .chassis import Chassis


class Router(Base):
    __tablename__ = "router"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    model = Column(String)
    chassis: Chassis = relationship(
        "Chassis", uselist=False, back_populates="router"
    )

    def __repr__(self) -> str:
        return (
            f"Router(id={self.id!r}, name={self.name!r}, model={self.model!r})"
        )

    @hybrid_property
    def active_port_count(self) -> int:
        return self.chassis.active_port_count

    @active_port_count.expression  # type:ignore[no-redef]
    def active_port_count(cls) -> int:
        return Chassis.active_port_count
