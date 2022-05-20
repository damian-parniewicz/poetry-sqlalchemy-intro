from sqlalchemy import Column, Integer, String

from ..common.base import Base


class Vlan(Base):
    __tablename__ = "vlanS"

    id = Column(Integer, primary_key=True)
    name = Column(String)
