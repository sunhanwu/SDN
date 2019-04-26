#! /usr/bin/env python
# -*- coding:utf-8 -*-
from mininet.net import Mininet
from mininet.node import Controller,RemoteController
from mininet.cli import CLI 
from mininet.log import setLogLevel,info
from mininet.link import Link,TCLink
from mininet.topo import Topo 
import logging
import os
import pdb


class LinearTopo(Topo):
    def __init__(self,length):
        logger.debug("Class LinearTopo init")
        self.switch_list=[]
        self.host_list=[]
        Topo.__init__(self)
        self.create_nodes(length)
        self.create_links(length)

    def create_nodes(self,length):
        for i in xrange(0,length):
            self.switch_list.append(self.addSwitch('s'+str(i)))
            self.host_list.append(self.addHost('h'+str(i)))

    def create_links(self,length):
        for i in xrange(0,length):
            self.addLink(self.switch_list[i],self.host_list[i])
        for i in xrange(0,length-1):
            self.addLink(self.switch_list[i],self.switch_list[i+1])
    
    def set_ovs_protocol_13(self):
        for sw in self.switch_list: 
            cmd="sudo ovs-vsctl set bridge %s protocols=OpenFlow13" 
            os.system(cmd)

#用于创建拓扑的函数
def create_topo(length):
    topo=LinearTopo(length)
    CONTROLLER_IP='127.0.0.1'
    CONTROLLER_PORT=6633
    net = Mininet(topo=topo,link=TCLink,controller=None)
    net.addController('controller',controller=RemoteController,ip=CONTROLLER_IP,port=CONTROLLER_PORT)
    net.start()
    topo.set_ovs_protocol_13()
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
        create_topo(3)
