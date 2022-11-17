from mininet.topo import Topo

class MyTopo(Topo):
    
    def __init__(self):
        
        Topo.__init__(self)
        
        H1=self.addHost('h1',ip="20.0.0.1")
        H2=self.addHost('h2',ip="20.0.0.2"

        S1=self.addSwitch('s1')
        S2=self.addSwitch('s2')
        S3=self.addSwitch('s3')
        S4=self.addSwitch('s4')
        SwitchList=(S1,S2,S3,S4)

        self.addLink(H1,S1)
        self.addLink(H2,S3)
        self.addLink(S1,S2)
        self.addLink(S1,S3)
        self.addLink(S1,S4)
        self.addLink(S2,S3)
        self.addLink(S2,S4)
        self.addLink(S3,S4)

topos={'mytopo': (lambda: MyTopo())}
