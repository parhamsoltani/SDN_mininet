from mininet.net import Mininet
from mininet.node import RemoteController,OVSKernelSwitch,DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topology():
    net=Mininet(
        controller=None,
        switch=OVSKernelSwitch,
        link=TCLink,
        autoSetMacs=True
    )

    #adding h1 and h2 hosts
    h1=net.addHost(
        name="h1",
        ip="10.10.105.22/24",
	mac="00:00:00:00:00:01",
	defaultRoute="via 10.0.1.1"
        )
    h2=net.addHost(
        name="h2",
        ip="10.10.105.22/24",
	mac="00:00:00:00:00:02",
	defaultRoute="via 10.0.2.1"
        )

    #adding s1 and s2 switches and r1 router
    s1=net.addSwitch(
        name="s1"
        )
    s2=net.addSwitch(
        name="s2"
        )
    r1=net.addSwitch(
	name="r1"
        )

    net.addLink(h1,s1)
    net.addLink(s1,r1)
    net.addLink(r1,s2)
    net.addLink(s2,h2)

    net.build()
    net.start()
    CLI(net)
    net.stop()

topology()
