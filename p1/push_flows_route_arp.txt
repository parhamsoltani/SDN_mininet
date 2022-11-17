#!/bin/bash
ovs-ofctl add-flow s2 in_port=2,actions=output:1

#the following flows added to handle arp in the r1 router
ovs-ofctl add-flow r1 arp,nw_src=10.0.1.1/24,nw_dst=10.0.2.1/24,actions=output:2
ovs-ofctl add-flow r1 arp,nw_src=10.0.2.1/24,nw_dst=10.0.1.1/24,actions=output:1
#r1 works as a router, so we add ip based flows, we also decrement TTL
ovs-ofctl add-flow r1 ip,nw_src=10.0.1.1/24,new_dst=10.0.2.1/24,actions=dec_ttl,output:2
ovs-ofctl add-flow r1 ip,nw_src=10.0.2.1/24,new_dst=10.0.1.1/24,actions=dec_ttl,output:1

#here we print the added flows, to see them in terminal
ovs-ofctl dump-flows s1
ovs-ofctl dump-flows r1
ovs-ofctl dump-flows s2

