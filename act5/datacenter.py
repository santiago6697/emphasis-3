# 11 switches, 1 web server, 1 video server, 1 remote controller (ryu)

import sys

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info

ryu_ip_address = sys.argv[1]
delay = sys.argv[2]
bw = int(sys.argv[3])
loss = float(sys.argv[4])

print("CONTROLLER IP ADDRESS: "+ryu_ip_address)
print("DELAY: "+delay)
print("BANDWIDTH: "+str(bw))
print("PACKET LOSS: "+str(loss))

def datacenter(ryu_ip_address, delay, bw, loss):
    switches = []

    # Declare racks' lists
    rack_one = []
    rack_two = []
    rack_three = []
    rack_four = []
    rack_five = []
    rack_six = []
    rack_seven = []
    rack_eight = []
    rack_nine = []
    rack_ten = []
    rack_eleven = []

    # Create a tree network without a local controller and constrained links
    net = Mininet(topo=None, build=False)
    # net = Mininet(controller=None, link=TCLink)

    # Adding remote controller
    # net.addController(name='c0')
    net.addController('c0', controller=RemoteController,
                      ip=ryu_ip_address, port=6633)

    # Adding 11 switches
    for i in range(0, 11):
        switches.append(net.addSwitch('s'+str(i+1)))

    # Adding 10 hosts for switch 1 and link them to it
    for i in range(0, 10):
        rack_one.append(net.addHost('h'+str(i+1)+'r1', ip='10.0.1.'+str(i+1)))
        net.addLink(switches[0], rack_one[i], delay=delay, bw=bw, loss=loss)

    # Adding 2 servers (hosts) for switch 1 and link them to it
    ws = net.addHost('ws', ip='10.0.1.20')
    vs = net.addHost('vs', ip='10.0.1.25')
    net.addLink(switches[0], ws, delay=delay, bw=bw, loss=loss)
    net.addLink(switches[0], vs, delay=delay, bw=bw, loss=loss)

    # Adding links for switches 2, 3, 7 and 11 to 1
    net.addLink(switches[0], switches[1], delay=delay, bw=bw, loss=loss)
    net.addLink(switches[0], switches[2], delay=delay, bw=bw, loss=loss)
    net.addLink(switches[0], switches[6], delay=delay, bw=bw, loss=loss)
    net.addLink(switches[0], switches[10], delay=delay, bw=bw, loss=loss)

    # Adding 40 hosts for switch 2 and link them to it
    for i in range(0, 40):
        rack_two.append(net.addHost('h'+str(i+1)+'r2', ip='10.0.2.'+str(i+1)))
        net.addLink(switches[1], rack_two[i], delay=delay, bw=bw, loss=loss)

    # Adding 20 hosts for switch 3 and link them to it
    for i in range(0, 20):
        rack_three.append(net.addHost('h'+str(i+1)+'r3', ip='10.0.3.'+str(i+1)))
        net.addLink(switches[2], rack_three[i], delay=delay, bw=bw, loss=loss)

    # Adding links for switches 4 and 5 to 3
    net.addLink(switches[2], switches[3], delay=delay, bw=bw, loss=loss)
    net.addLink(switches[2], switches[4], delay=delay, bw=bw, loss=loss)

    # Adding 10 hosts for switch 4 and link them to it
    for i in range(0, 10):
        rack_four.append(net.addHost('h'+str(i+1)+'r4', ip='10.0.4.'+str(i+1)))
        net.addLink(switches[3], rack_four[i], delay=delay, bw=bw, loss=loss)
    
    # Adding 30 hosts for switch 5 and link them to it
    for i in range(0, 30):
        rack_five.append(net.addHost('h'+str(i+1)+'r5', ip='10.0.5.'+str(i+1)))
        net.addLink(switches[4], rack_five[i], delay=delay, bw=bw, loss=loss)

    # Adding 10 hosts for switch 6 and link them to it
    for i in range(0, 10):
        rack_six.append(net.addHost('h'+str(i+1)+'r6', ip='10.0.6.'+str(i+1)))
        net.addLink(switches[5], rack_six[i], delay=delay, bw=bw, loss=loss)

    # Adding 20 hosts for switch 7 and link them to it
    for i in range(0, 20):
        rack_seven.append(net.addHost('h'+str(i+1)+'r7', ip='10.0.7.'+str(i+1)))
        net.addLink(switches[6], rack_seven[i], delay=delay, bw=bw, loss=loss)

    # Adding links for switch 9 to 7
    net.addLink(switches[6], switches[8], delay=delay, bw=bw, loss=loss)

    # Adding 10 hosts for switch 8 and link them to it
    for i in range(0, 10):
        rack_eight.append(net.addHost('h'+str(i+1)+'r8', ip='10.0.8.'+str(i+1)))
        net.addLink(switches[7], rack_eight[i], delay=delay, bw=bw, loss=loss)

    # Adding links for switches 9 and 6 to 8
    net.addLink(switches[7], switches[5], delay=delay, bw=bw, loss=loss)
    net.addLink(switches[7], switches[8], delay=delay, bw=bw, loss=loss)

    # Adding 10 hosts for switch 9 and link them to it
    for i in range(0, 10):
        rack_nine.append(net.addHost('h'+str(i+1)+'r9', ip='10.0.9.'+str(i+1)))
        net.addLink(switches[8], rack_nine[i], delay=delay, bw=bw, loss=loss)

    # Adding 40 hosts for switch 10 and link them to it
    for i in range(0, 40):
        rack_ten.append(net.addHost('h'+str(i+1)+'r10', ip='10.0.10.'+str(i+1)))
        net.addLink(switches[9], rack_ten[i], delay=delay, bw=bw, loss=loss)
    
    # Adding links for switch 11 to 10
    net.addLink(switches[9], switches[10], delay=delay, bw=bw, loss=loss)

    # Adding 20 hosts for switch 11 and link them to it
    for i in range(0, 20):
        rack_eleven.append(net.addHost('h'+str(i+1)+'r11', ip='10.0.11.'+str(i+1)))
        net.addLink(switches[10], rack_eleven[i], delay=delay, bw=bw, loss=loss)

    # Starting network
    net.start()

    # Dumping host connections
    dumpNodeConnections(net.hosts)

    CLI(net)

    ws.cmd('python -m SimpleHTTPServer 10.0.1.20:80 &')

if __name__ == '__main__':
    setLogLevel('info')
    datacenter(ryu_ip_address, delay, bw, loss)

