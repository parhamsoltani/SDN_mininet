from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topology():
    net = Mininet (controller=RemoteController,Switch=OVSKernelSwitch,link=TCLink,autoSetMacs=True)
    # Adding ODL controller
    odl_controller=net.addController(name="ODL_Controller",ip="127.0.1.1",port=6633)
    # Adding 8 hosts
    hosts=[]
    for i in range(1,9):
        hosts.append(net.addHost(name="Host"+str(i),ip="10.0.0."+str(i)+"/24",mac="00:00:00:00:00:0"+str(i)))

    # Adding four switches on third stage
    switches_third_stage=[]
    for i in range(1,5):
        switches_third_stage.append(net.addSwitch(name="S3"+str(i),protocols="OpenFlow13"))
        # Starting controller on the switch
        switches_third_stage[i-1].start([odl_controller])
        # Adding links from third stage switches to the hosts
        net.addLink(switches_third_stage[i-1],hosts[2*(i-1)])
        net.addLink(switches_third_stage[i-1],hosts[2*(i-1)+1])

    # Adding two switches on second stage
    switches_second_stage=[]
    for i in range(1,3):
        switches_second_stage.append(net.addSwitch(name="S2"+str(i),protocols="OpenFlow13"))
        # Starting controller on the switch
        switches_second_stage[i-1].start([odl_controller])
        # Adding links from second stage switches to the third stage switches
        net.addLink(switches_second_stage[i-1],switches_third_stage[2*(i-1)])
        net.addLink(switches_second_stage[i-1],switches_third_stage[2*(i-1)+1])
    # Adding root switch
    switches_root=[]
    for i in range(1,2):
        switches_root.append(net.addSwitch(name="SR1",protocols="OpenFlow13"))
        # Starting controller on the switch
        switches_root[i-1].start([odl_controller])
        # Adding links from root switches to the second stage switches
        net.addLink(switches_root[i-1],switches_second_stage[2*(i-1)])
        net.addLink(switches_root[i-1],switches_second_stage[2*(i-1)+1])
    net.build()
    net.start()
    CLI(net)
    net.stop()

topology()
