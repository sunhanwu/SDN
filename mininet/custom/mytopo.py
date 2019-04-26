"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo


class MyTopo(Topo):
    "Simple topology example."

    def __init__(self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__(self)

        # add some hosts
        Host1 = self.addHost('H1')
        Host2 = self.addHost('H2')
        Host3 = self.addHost('H3')
        Host4 = self.addHost('H4')
        Host5 = self.addHost('H5')
        Host6 = self.addHost('H6')
        Host7 = self.addHost('H7')
        Host8 = self.addHost('H8')
        # add some switches
        Switches1=self.addSwitch('S1')
        Switches2=self.addSwitch('S2')
        Switches3=self.addSwitch('S3')
        Switches3=self.addSwitch('S4')
        # add some Links
            # 交换机和主机之间的连接
        self.addLink(Host1,Switches1)
        self.addLink(Host2,Switches1)
        self.addLink(Host3,Switches2)
        self.addLink(Host4,Switches2)
        self.addLink(Host5,Switches3)
        self.addLink(Host6,Switches3)
            # 交换机和交换机之间的连接
        self.addLink(Switches1,Switches2)
        self.addLink(Switches2,Switches3)

topos = {'mytopo': (lambda: MyTopo())}
