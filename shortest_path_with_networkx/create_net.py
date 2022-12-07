from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topology():
    # Reading the input weight matrix from a text file
    with open('Weight_Mat.txt','r') as f:
        Weight_Mat = [[int(num) for num in line.split(',')] for line in f]

    # Net Parameters
    net = Mininet (controller=RemoteController,Switch=OVSKernelSwitch,link=TCLink,autoSetMacs=True)
    
    # Adding ODL controller
    odl_controller=net.addController(name="ODL_Controller",ip="127.0.1.1",port=6633)
    
    # Adding Hosts (For node "1" and node "n" only)
    hosts=[]
    for i in range(1,3):
        hosts.append(net.addHost(name="Host" + str(i-1), ip="10.0."+str(i)+".1"+"/24",mac="00:00:00:00:00:0"+str(i),defaultRoute="via 10.0."+str(i)+".1"))
        
    # Adding all switches (equal to the number of rows in Matrix)
    switches=[]
    for i in range(1, len(Weight_Mat)+1):
        switches.append(net.addSwitch(name="S" + str(i), protocols="OpenFlow13"))

    # Adding Links
    for i in range(0, len(Weight_Mat)):
        if i==0: # Link from node "1" to its host
            net.addLink(switches[i], hosts[0])
        if i==len(Weight_Mat) - 1 : # Link from node "n" to its host
            net.addLink(switches[i], hosts[1])
        for j in range(i+1, len(Weight_Mat)):
            if Weight_Mat[i][j] != 0 or Weight_Mat[j][i] != 0:
                net.addLink(switches[i], switches[j])

    # Starting controller on the switch
    for i in range(0, len(Weight_Mat)):
        switches[i].start([odl_controller])

    net.build()
    net.start()
    CLI(net)
    net.stop()

topology()
