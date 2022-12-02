from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topology():
    net = Mininet (controller=RemoteController,Switch=OVSKernelSwitch,link=TCLink,autoSetMacs=True)
    # Adding ODL controller
    odl_controller=net.addController(name="ODL_Controller",ip="127.0.1.1",port=6633)
    # Adding 2 hosts
    hosts=[]
    for i in range(1,3):
        hosts.append(net.addHost(name="Host"+str(i),ip="10.0."+str(i)+".1"+"/24",mac="00:00:00:00:00:0"+str(i),defaultRoute="via 10.0"+str(i)+".1")))

    # Adding three switches
    switches=[]
    for i in range(1,4):
        switches.append(net.addSwitch(name="S1"+str(i),protocols="OpenFlow13"))
        # Starting controller on the switch
        switches[i-1].start([odl_controller])
    # Adding links
    for i in range(1,4):
        if i==1:
            net.addLink(switches[i-1],hosts[0])
        if i==2:
            net.addLink(switches[i-1],hosts[i-2])
            net.addLink(switches[i-1],hosts[i])
        if i==3:
            net.addLink(switches[i-1],hosts[1])
    net.build()
    net.start()
    CLI(net)
    net.stop()

topology()
                
