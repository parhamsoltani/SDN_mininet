#!/bin/sh

#First we clean all switches from flows
ovs-ofctl del-flows s1
ovs-ofctl del-flows s2
ovs-ofctl del-flows s3

#to reduce the number of flows we use general flows for ARPs
#switch1
ovs-ofctl add-flow s1 arp,actions=push_mpls:0x8847,set_field:40-\>mpls_label,output:2
ovs-ofctl add-flow s1 dl_type=0x8847,mpls_label=40,actions=pop_mpls:0x806,output:1

#switch2
ovs-ofctl add-flow s2 arp,actions=push_mpls:0x8847,set_field:40-\>mpls_label,output:2,output:3
ovs-ofctl add-flow s1 dl_type=0x8847,mpls_label=40,actions=output:2,output:3,pop_mpls:0x806,output:1

#switch3
ovs-ofctl add-flow s3 arp,actions=push_mpls:0x8847,set_field:40-\>mpls_label,output:2
ovs-ofctl add-flow s3 dl_type=0x8847,mpls_label=40,actions=pop_mpls:0x806,output:1

#Ip handling
#host1 to host3 setting label
ovs-ofctl add-flow s1 ip,nw_src=10.0.0.1,nw_dst=10.0.0.3,actions=push_mpls:0x8847,set_field:10-\>mpls_label,output:2
#host1 to host2 setting label
ovs-ofctl add-flow s1 ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=push_mpls:0x8847,set_field:20-\>mpls_label,output:2
#own packet
ovs-ofctl add-flow s1 dl_type=0x8847,mpls_label=10,actions=pop_mpls:0x806,output:1

#host2 to host1 setting label
ovs-ofctl add-flow s2 ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=push_mpls:0x8847,set_field:10-\>mpls_label,output:2
#host2 to host3 setting label
ovs-ofctl add-flow s2 ip,nw_src=10.0.0.2,nw_dst=10.0.0.3,actions=push_mpls:0x8847,set_field:30-\>mpls_label,output:3
#transparency(h1 to h3) changing the label
ovs-ofctl add-flow s2 dl_type=0x8847,mpls_label=10,actions=set_field:30-\>mpls_label,output:3
#transparency(h3 to h1) changing the label
ovs-ofctl add-flow s2 dl_type=0x8847,mpls_label=30,actions=set_field:10-\>mpls_label,output:2
#own packet
ovs-ofctl add-flow s2 dl_type=0x8847,mpls_label=20,actions=pop_mpls:0x0800,output:1

#host3 to host1 setting label
ovs-ofctl add-flow s3 ip,nw_src=10.0.0.3,nw_dst=10.0.0.1,actions=push_mpls:0x8847,set_field:30-\>mpls_label,output:2
#host3 to host2 setting label
ovs-ofctl add-flow s3 ip,nw_src=10.0.0.3,nw_dst=10.0.0.2,actions=push_mpls:0x8847,set_field:20-\>mpls_label,output:2
#own packet
ovs-ofctl add-flow s3 dl_type=0x8847,mpls_label=30,actions=pop_mpls:0x0800,output:1