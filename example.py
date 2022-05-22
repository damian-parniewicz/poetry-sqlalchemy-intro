from copy import deepcopy
from pprint import pformat

from sqlalchemy import select

from poetry_sqlalchemy_intro.common.base import Session
from poetry_sqlalchemy_intro.domain import Card, Chassis, Port, Router, Vlan
from poetry_sqlalchemy_intro.domain.port import EthernetSpeed


def create_switch(router_name: str) -> None:
    router = Router(
        name=router_name, model="Juniper MX960", chassis=Chassis(max_slots=14)
    )
    card = Card(
        max_ports=8,
        ports=[
            Port(speed=EthernetSpeed.Ethernet_100G),
            Port(speed=EthernetSpeed.Ethernet_100G),
            Port(speed=EthernetSpeed.Ethernet_100G),
            Port(speed=EthernetSpeed.Ethernet_100G),
        ],
    )
    router.chassis.cards = [deepcopy(card), card]

    with Session() as session:
        session.add(router)
        session.commit()

        print(f"Router `{router.name}` created")
        print(f"Router has {router.active_port_count} active ports")


def count_ports(router_name: str) -> int:
    with Session() as session:
        stm = select(Router).where(Router.name == router_name)
        router = session.scalars(stm).one()

        ports = session.query(Port).all()
        print(f"All ports in DB are:\n{pformat(ports)}")

        port_count = router.active_port_count
        print(f"Router {router_name} has {port_count} active ports")
        return port_count


def create_vlans() -> None:
    vlan_blue = Vlan(name="VLAN blue")
    vlan_red = Vlan(name="VLAN red")
    print(f"\nVlan before assignment: {pformat(vlan_blue)}")

    with Session() as session:
        session.add(vlan_blue)
        session.commit()
        ports = session.query(Port).all()

        for port_index in [1, 2, 3]:
            vlan_blue.ports.append(ports[port_index])

        for port_index in [0, 2, 3]:
            ports[port_index].vlans.append(vlan_red)

        print(f"Vlan after assignment: {pformat(vlan_blue)}")
        print(f"Vlan after assignment: {pformat(vlan_red)}")

        session.commit()


def check_vlans() -> None:
    with Session() as session:
        vlans = session.query(Vlan).all()
        print(f"Queried vlans are: {vlans}")


def main() -> int:
    router_name = "Lab-router-1"
    create_switch(router_name)
    count_ports(router_name)
    create_vlans()
    check_vlans()
    return 0


if __name__ == "__main__":
    exit(main())
