#!/usr/bin/python

from time import time
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info

import matplotlib.pyplot as plt

def treeNet(requests, times):
    elapsed_time = []
    request_number = []
    # Create a tree network without a local controller and constrained links
    net = Mininet(controller=None, link=TCLink)

    # Adding remote controller
    # net.addController('c1', controller=RemoteController,
    #                   ip='127.0.0.1', port=6633)

    # Adding hosts
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')

    # Adding switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Creating core links 100Mbps, 100ms delay and user links 1000Mbps and 1ms delay
    # net.addLink( h4p, s3, bw=1000, delay='1ms' )
    net.addLink(s2, s1, bw=100)
    net.addLink(s3, s1, bw=100)
    net.addLink(h1, s2, bw=100)
    net.addLink(h2, s2, bw=100)
    net.addLink(h3, s3, bw=100)
    net.addLink(h4, s3, bw=100)

    # Starting network
    net.start()

    # Dumping host connections
    dumpNodeConnections(net.hosts)

    # CLI(net)
    print(s1.cmd('ovs-ofctl add-flow s1 priority=500,ip,nw_proto=6,tp_dst=80,actions=output:1'))
    print(s1.cmd('ovs-ofctl add-flow s1 priority=500,ip,nw_proto=6,tp_dst=80,actions=output:2'))
    print(s2.cmd('ovs-ofctl add-flow s2 priority=500,ip,nw_proto=6,tp_dst=80,actions=output:3'))
    print(s2.cmd('ovs-ofctl add-flow s2 priority=500,ip,nw_proto=6,tp_dst=80,actions=output:1'))
    print(s3.cmd('ovs-ofctl add-flow s3 priority=500,ip,nw_proto=6,tp_dst=80,actions=output:3'))
    print(s3.cmd('ovs-ofctl add-flow s3 priority=500,ip,nw_proto=6,tp_dst=80,actions=output:1'))

    h3.cmd('python -m SimpleHTTPServer 10.0.0.3:80')
    for tm in range(times):
        start = time()
        for request in range((tm+1)*requests):
            h1.cmd('wget 10.0.0.3')
        end = time()
        total = (end-start)*1000
        elapsed_time.append(total)
        request_number.append(int(tm+1))
        print(str(tm+1)+"  "+str(total))

    net.stop()

    plt.plot(request_number, elapsed_time)
    plt.show()


if __name__ == '__main__':
    setLogLevel('info')
    treeNet(100, 5)
