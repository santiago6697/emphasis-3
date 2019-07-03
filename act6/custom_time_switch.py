from datetime import datetime
# from ryu import cfg
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import icmp
from ryu.lib.packet import ipv4

'''
CONF = cfg.CONF
CONF.register_opts([
    cfg.IntOpt('start', default=12),
    cfg.IntOpt('end', default=17),
    cfg.StrOpt('src', default='10.0.0.1'),
    cfg.StrOpt('dst', default='10.0.0.2'),
    cfg.Opt('disconnect', default=False)
])

print('disc: ' + CONF.disconnect)
'''

class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        config_file = open('time_switch.conf', 'r')
        configs = config_file.readlines()
        config_file.close()

        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser

        #print('test-param-str = %s' % self.CONF.test_param_str1)

        pkt = packet.Packet(msg.data)
        #iph = pkt.get_protocol(ipv4.ipv4)
        #print('hihi'+str(ofp_parser))
        #if(len(pkt.get_protocols(ipv4.ipv4)) > 0):

        #self.logger.info("packet-in %s" % (pkt,))
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)        
        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        if pkt_ipv4:
            #self.logger.info("src %s" % (pkt_ipv4.src,))

            dst = str(pkt_ipv4.dst).strip()
            src = str(pkt_ipv4.src).strip()
            crnt_time = datetime.now().hour
            disconnect = False

            for ins in configs:
                if 'disconnect' in ins:
                    disconnect = True
                if 'start' in ins:
                    start_hour = datetime.strptime(ins.split(' ')[1], '%H:%M:%S').time
                if 'end' in ins:
                    end_hour = datetime.strptime(ins.split(' ')[1], '%H:%M:%S').time
                if 'dst' in ins:
                    drop_dst = str(ins.split(' ')[1]).strip()
                if 'src' in ins:
                    drop_src = str(ins.split(' ')[1]).strip()

            #self.logger.info("dsrc %s ddst %s st %d en %d" % (drop_src,drop_dst,start_hour,end_hour,))
            
            if disconnect:
                #self.logger.info("dest %s" % (drop_dst,))
                if crnt_time >= start_hour and crnt_time <= end_hour:
                    #self.logger.info("crnt %s" % (crnt_time,))
                    #self.logger.info("dst %s drop_dst %s src %s drop_src %s" % (dst,drop_dst,src,drop_src,))
                    if dst == drop_dst and src == drop_src:
                        #self.logger.info("hi")
                        actions = []

        #actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        out = ofp_parser.OFPPacketOut(
            datapath=dp, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions)
        dp.send_msg(out)
