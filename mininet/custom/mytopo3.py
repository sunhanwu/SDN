# -*- coding:utf-8 -*-
from mininet.net import  Mininet
from mininet.node import Controller,RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel,info
from mininet.link import Link,Intf,TCLink
from mininet.topo import Topo
import logging
import os


def mutiControllerNet(con_num=3,sw_num=4,host_num=8):
    "Create a network from semi-scratch with mutiple controller"
    controller_list=[]
    switch_list=[]
    host_list=[]
    
    #创建SDN网络
    net = Mininet(controller=None,switch=OVSSwitch,link=TCLink)

    # 这里原来是自动控制器的源代码，现在改成自定义控制器Ip
    # c1=RemoteController('c1',ip='127.0.0.1',port=1234)
    c2=RemoteController('c2',ip='192.168.43.144',port=6633)
    # c3=RemoteController('c3',ip='127.0.0.1',port=1236)
    #  c1=Controller('c1',port=1234)
    # c2=Controller('c2',port=1235)
    #  c3=Controller('c3',port=1236)
    
    # 加入网络
    net.addController(c1)
    #  net.addController(c2)
    #  net.addController(c3)

    #加入控制器数组
    controller_list.append(c1)
    controller_list.append(c2)
    controller_list.append(c3)

    #创建交换机
    print "*** 创建交换机"
    switch_list = [net.addSwitch('s%d'% n) for n in xrange(sw_num)]

    #创建主机
    print "*** Create hosts"
    host_list = [net.addHost('h%d' % n) for n in xrange(host_num)]

    #创建主机到交换机之间的连接
    net.addLink(switch_list[0],host_list[0])
    net.addLink(switch_list[0],host_list[1])
    net.addLink(switch_list[1],host_list[2])
    net.addLink(switch_list[1],host_list[3])
    net.addLink(switch_list[2],host_list[4])
    net.addLink(switch_list[2],host_list[5])
    net.addLink(switch_list[3],host_list[6])
    net.addLink(switch_list[3],host_list[7])

    #创建交换机和交换机之间的连接
    print "*** 创建交换机之间的连接"
    net.addLink(switch_list[0],switch_list[1])
    net.addLink(switch_list[1],switch_list[2])
    net.addLink(switch_list[2],switch_list[3])

    #创建交换机和控制器之间的连接
    # print "***创建交换机和控制器之间的连接"
    print "*** Staring network"
    net.build()
    for c in controller_list:
        c.start()

    _No = 0
    for i in xrange(0,sw_num,sw_num/con_num):
        for j in xrange(sw_num/con_num):
            switch_list[i+j].start([controller_list[_No]])

    print "*** Runing CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    mutiControllerNet(con_num=3,sw_num=4,host_num=8)


    





