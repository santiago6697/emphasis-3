#!/usr/bin/python
# Number of requests, controller ip address, type of conducted test, file generated
import sys

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info

# requests_number = sys.argv[0]
# controller_ip = sys.argv[1]
# test_type = sys.argv[2]


def treeNet():
    # Create a tree network without a local controller and constrained links
    net = Mininet(controller=None, link=TCLink)

    # Adding remote controller
    # net.addController('c1', controller=RemoteController,
    #                   ip='127.0.0.1', port=6633)

    # Adding hosts
    # h1a = net.addHost( 'h1a', ip='10.0.0.1' )
    # h2p = net.addHost( 'h2p', ip='10.0.0.2' )
    # h3p = net.addHost( 'h3p', ip='10.0.0.3' )
    # h4p = net.addHost( 'h4p', ip='10.0.0.4' )
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')

    # Adding switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Creating core links 100Mbps, 100ms delay and user links 1000Mbps and 1ms delay
    # net.addLink( s2, s1, bw=100, delay='100ms' )
    # net.addLink( s3, s1, bw=100, delay='100ms' )
    # net.addLink( h1a, s2, bw=1000, delay='1ms' )
    # net.addLink( h2p, s2, bw=1000, delay='1ms' )
    # net.addLink( h3p, s3, bw=1000, delay='1ms' )
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

    print(s1.cmd('ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,actions=output:2'))
    print(s1.cmd('ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,actions=output:1'))
    print(s2.cmd('ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,actions=output:3'))
    print(s2.cmd('ovs-ofctl add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,actions=output:1'))
    print(s3.cmd('ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,actions=output:2'))
    print(s3.cmd('ovs-ofctl add-flow s3 dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,actions=output:3'))

    print(s1.cmd('ovs-ofctl add-flow s1 actions=normal'))
    print(s2.cmd('ovs-ofctl add-flow s2 actions=normal'))
    print(s3.cmd('ovs-ofctl add-flow s3 actions=normal'))

    print(h4.cmd('python -m SimpleHTTPServer 80 &'))

    # print(h1.cmd('python request.py 100'))
    # print(h1.cmd('python request.py 200'))
    # print(h1.cmd('python request.py 300'))
    # print(h1.cmd('python request.py 400'))
    # print(h1.cmd('python request.py 500'))

    # print(h1.cmd('python script.py'))

    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    treeNet()
