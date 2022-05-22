from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..common.base import Base

vlan_assignments = Table(
    "vlan_assignments",
    Base.metadata,
    Column("vlan_id", ForeignKey("vlan.id"), primary_key=True),
    Column("port_id", ForeignKey("port.id"), primary_key=True),
)


class Vlan(Base):
    __tablename__ = "vlan"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ports = relationship("Port", secondary=vlan_assignments, backref="vlans")

    def __repr__(self) -> str:
        port_ids = [port.id for port in self.ports]
        return (
            f"Vlan(id={self.id!r}, name={self.name!r}, " f" ports={port_ids}))"
        )
