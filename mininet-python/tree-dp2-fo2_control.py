#!/usr/bin/python

from time import time, sleep
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info

import requests as http

import matplotlib.pyplot as plt


def treeNet(requests):
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

    print(s2.cmd('ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,actions=output:3'))
    print(s1.cmd('ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,actions=output:2'))
    print(s3.cmd('ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,actions=output:2'))
    print(s3.cmd('ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,actions=output:3'))
    print(s1.cmd('ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,actions=output:1'))
    print(s2.cmd('ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,actions=output:1'))

    print(s1.cmd('ovs-ofctl add-flow s1 arp,nw_proto=1,actions=flood'))
    print(s2.cmd('ovs-ofctl add-flow s2 arp,nw_proto=1,actions=flood'))
    print(s3.cmd('ovs-ofctl add-flow s3 arp,nw_proto=1,actions=flood'))

    CLI(net)

    # h3.cmd('python -m SimpleHTTPServer 10.0.0.4:80')

    # requests_time = []
    # request_number = []

    # sec_per_req = 60/float(requests)
    # for request in range(requests):
    #     start = time()
    #     contents = http.get("http://10.0.0.4")
    #     # print(contents)
    #     total = (time() - start)
    #     print('in ' + str(total) + ' s')
    #     # output.writelines(str(total)+'\n')
    #     # print(str(trip_time))
    #     if sec_per_req > total:
    #             sleep(sec_per_req - total)

    #     # start = time()
    #     # h1.cmd('wget 10.0.0.4')
    #     # end = time()
    #     # total = (end-start)*1000
    #     requests_time.append(total)
    #     request_number.append(request+1)

    # plt.plot(request_number, requests_time)
    # plt.show()

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    treeNet(500)
