#! /usr/bin/env python
# -*- coding:utf-8 -*-
from mininet.net import Mininet
from mininet.node import Controller,RemoteController,OVSSwitch,OVSController
from mininet.cli import CLI 
from mininet.log import setLogLevel,info
from mininet.link import Link,TCLink
from mininet.topo import Topo 
import logging
import os
import pdb

c0 = RemoteController( 'c2', ip='127.0.0.1', port=6633 )
c1 = RemoteController( 'c2', ip='127.0.0.1', port=6633 )
c2 = RemoteController( 'c2', ip='127.0.0.1', port=6633 )
c3 = RemoteController( 'c2', ip='127.0.0.1', port=6633 )
#  c4 = RemoteController( 'c2', ip='127.0.0.1', port=6633 )

cmap = {'s0':c0,'s1':c0,'s2':c1,'s3':c1,'s4':c2,'s5':c2,'s6':c3,'s7':c3}


class MutiController(Topo):
    def __init__(self):
        logger.debug("Class MutiController init")
        self.switch_list=[]
        self.host_list=[]
        Topo.__init__(self)
        self.create_nodes()
        self.create_links()
        #  self.hopts={'defaultRoute':'via 10.0.0.254'}
        #  pdb.set_trace()
        #  h15.cmdPrint('dhclient '+h15.defaultIntf().name)
        
    #  def build(self,NatIP='10.0.0.254'):
        #  self.hopts={'defaultRoute':'via'+NatIP}
        #  nat1=self.addNode('nat1',cls=NAT,ip=NatIP,inNamespace=False)
        #  self.addLink(nat1,self.switch_list[0])

    def create_nodes(self):
        for i in xrange(0,8):
            self.switch_list.append(self.addSwitch('s'+str(i)))
        #  pdb.set_trace()
        for j in xrange(0,16):
            self.host_list.append(self.addHost('h'+str(j)))
        #  self.host_list.append(self.addNode('nat1',cls=NAT,ip='10.0.0.254',inNamespace=False))
        #  self.host_list.append(self.addHost('h15',ip='0.0.0.0'))
      #  h15=self.host_list[-1]
    
    def create_links(self):
        for i in xrange(0,8):
            self.addLink(self.switch_list[i],self.host_list[i*2])
            self.addLink(self.switch_list[i],self.host_list[i*2+1])
        for j in xrange(0,3):
            #  pdb.set_trace()
            self.addLink(self.switch_list[j],self.switch_list[j+1])
        for k in xrange(5,7):
            self.addLink(self.switch_list[k],self.switch_list[k+1])
    
    def set_ovs_protocol_13(self):
        for sw in self.switch_list: 
            cmd="sudo ovs-vsctl set bridge %s protocols=OpenFlow13" 
            os.system(cmd)

class MultiSwitch(OVSSwitch):
    def start(self,controllers):
        return OVSSwitch.start(self,[ cmap[ self.name]])

def create_topo():
    topo=MutiController()
    net = Mininet(topo=topo,switch=MultiSwitch,build=False,link=TCLink,controller=RemoteController)
    #  pdb.set_trace()
    #  net.addLink(topo.switch_list[0],h15)
    net.build()
    #  self.hopts={'defaultRoute':'via 10.0.0.254'}
    #  nat1=net.hosts[-1]
    #  net.addLink(nat1,net.switches[0])
    net.addNAT().configDefault()
    net.start()
    #  os.popen('ovs-vsctl add-port s7 enp0s3')
    #  h15.cmdPrint('dhclient '+h15.defaultIntf().name)
    CLI(net)
    net.stop()

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    setLogLevel('info')
    #  lineartopo=LinearTopo(3)
    #  pdb.set_trace()
    if os.getuid()!=0:
        logger.debug("You are NOT root!")
    elif os.getuid()==0:
        create_topo()

     
