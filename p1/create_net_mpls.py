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

    #adding hosts
    h1=net.addHost(
        name="h1",
        ip="10.10.0.1/24",
	mac="00:00:00:00:00:01"
        )
    h2=net.addHost(
        name="h2",
        ip="10.10.0.2/24",
	mac="00:00:00:00:00:02"
        )
    h3=net.addHost(
        name="h3",
        ip="10.10.0.3/24",
	mac="00:00:00:00:00:03"
        )

    #adding s1 and s2 and s3 switches 
    s1=net.addSwitch(
        name="s1"
        )
    s2=net.addSwitch(
        name="s2"
        )
    s3=net.addSwitch(
	name="s3"
        )

    net.addLink(h1,s1)
    net.addLink(h2,s2)
    net.addLink(h3,s3)
    net.addLink(s1,s2)
    net.addLink(s2,s3

    net.build()
    net.start()
    CLI(net)
    net.stop()

topology()
