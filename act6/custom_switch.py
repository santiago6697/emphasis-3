import sys
from datetime import datetime

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0, inet
from ryu.lib.packet import ipv4, packet, arp, ethernet

# host_a = sys.argv[2]
# host_b = sys.argv[3]
# start_time = datetime.strptime(sys.argv[4], '%H:%M').time()
# end_time = datetime.strptime(sys.argv[5], '%H:%M').time()

# host_a = "10.0.0.1"
# host_b = "10.0.0.4"
# start_time = datetime.strptime("10:00", '%H:%M').time()
# end_time = datetime.strptime("23:30", '%H:%M').time()


# print(host_a == host_b)
# print(start_time < current_time < end_time)


class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        host_a = "10.0.0.7" #h2r3
        host_b = "10.0.0.16" #h4r4
        start_time = datetime.strptime("23:42:00", '%H:%M:%S').time()
        end_time = datetime.strptime("23:42:30", '%H:%M:%S').time()
        msg = ev.msg
        dp = msg.datapath
        dpid = dp.id
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser

        pkt = packet.Packet(msg.data)
        # DEPRECATED:
        # try:
        #     header = pkt.get_protocol(arp.arp)
        #     src_ip = header.src_ip
        #     dst_ip = header.dst_ip
        #     print("ARP: "+header)
        # except:
        #     header = pkt.get_protocol(ipv4.ipv4)
        #     # src_ip = header.src
        #     # dst_ip = header.dst
        #     print("IPv4: "+header)
        arp_pkt = pkt.get_protocol(arp.arp)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)

        if arp_pkt:
            header = pkt.get_protocol(arp.arp)
            src_ip = header.src_ip
            dst_ip = header.dst_ip
            # print("ARP: "+str(header))
            print("ARP")
        elif ip_pkt:
            header = pkt.get_protocol(ipv4.ipv4)
            src_ip = header.src
            dst_ip = header.dst
            # print("IPv4: "+str(header))
            print("IPv4")
        else:
            # print("GO F YOURSELF")
            print("NO PROTOCOL MATCH")
        # src_ip = header.src_ip
        # dst_ip = header.dst_ip
        # print((src_ip == host_a and dst_ip == host_b) or (src_ip == host_b and dst_ip == host_a))
        if ((src_ip == host_a and dst_ip == host_b) or (src_ip == host_b and dst_ip == host_a)):
            current_time = datetime.now().time()
            print(start_time <= current_time <= end_time)
            if start_time <= current_time <= end_time:
                print("BLACK LIST, TIME FILTER")
                # Don't know why is this commented code so FUBU.
                # inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [])]
                # out = ofp_parser.OFPFlowMod(datapath=dp,
                #         # out_port=ofp.OFPP_ANY,
                #         # out_group=ofp.OFPG_ANY,
                #         # match=match, 
                #         # instructions=inst
                #         ) 
                # dp.send_msg(out)
                print("DROPING PACKETS")
            else:
                print("BLACK LIST, NO TIME FILTER")
                actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
                out = ofp_parser.OFPPacketOut(
                    datapath=dp, buffer_id=msg.buffer_id, in_port=msg.in_port,
                    actions=actions)
                dp.send_msg(out)
        else:
            print("NO BLACK LIST, NO TIME FILTER")
            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
            out = ofp_parser.OFPPacketOut(
                datapath=dp, buffer_id=msg.buffer_id, in_port=msg.in_port,
                actions=actions)
            dp.send_msg(out)