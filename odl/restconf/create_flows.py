import os
# This function writes the generated flow as a .xml file.
def write_xml(XML_Data, Name_of_File):
    with open(str(Name_of_File) + ".xml", 'wt') as f:
        f.write(XML_Data)
    f.close()

# This function creates L2 switching flows which is based on the in_port and out_port
# Note that switches will forward every packet in the opposite port
def flow_inport_outport(in_port,out_port,flow_num):
    XML_Output = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <flow xmlns="urn:opendaylight:flow:inventory">
                    <strict>false</strict>
                    <instructions>
                        <instruction>
                            <order>0</order>
                            <apply-actions>
                                <action>
                                    <order>0</order>
                                    <output-action>
                                        <output-node-connector>{}</output-node-connector>
                                    </output-action>
                                </action>
                            </apply-actions>
                        </instruction>
                    </instructions>
                    <table_id>0</tabel_id>
                    <id>{}</id>
                    <match>
                        <in-port>{}</in-port>
                    </match>
                </flow>
                """.format(out_port, flow_num, in_port)
    return XML_Output

# This function creates L3 switching flows, So the match fields are src/dst ip address.
# The action is forwarding the packet to the mentioned port.

def flow_ip_L3(out_port, flow_num, src_ip_addr, dst_ip_addr):
    XML_Output = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <flow xmlns="urn:opendaylight:flow:inventory">
                    <strict>false</strict>
                    <instructions>
                        <instruction>
                            <order>0</order>
                            <apply-actions>
                                <action>
                                    <order>0</order>
                                    <dec-nw-ttl/>
                                </action>
                                <action>
                                    <order>1</order>
                                    <output-action>
                                        <output-node-connector>{}</output-node-connector>
                                    </output-action>
                                </action>
                            </apply-actions>
                        </instruction>
                    </instructions>
                    <table_id>0</tabel_id>
                    <id>{}</id>
                    <match>
                        <ipv4-source>{}</ipv4-source>
                        <ipv4-destination>{}</ipv4-destination>
                        <ethernet-match>
                            <ethernet-type>
                                <type>2048</type>
                            </ethernet-type>
                        </ethernet-match>
                    </match>
                </flow>
                """.format(out_port, flow_num, src_ip_addr, dst_ip_addr)
    return XML_Output

# This function forward ARP packets.
def flow_arp_L3(out_port, flow_num, src_ip_addr, dst_ip_addr):
    XML_Output = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <flow xmlns="urn:opendaylight:flow:inventory">
                    <strict>false</strict>
                    <instructions>
                        <instruction>
                            <order>0</order>
                            <apply-actions>
                                <action>
                                    <order>0</order>
                                    <output-action>
                                        <output-node-connector>{}</output-node-connector>
                                    </output-action>
                                </action>
                            </apply-actions>
                        </instruction>
                    </instructions>
                    <table_id>0</tabel_id>
                    <id>{}</id>
                    <match>
                        <ethernet-match>
                            <ethernet-type>
                                <type>2054</type>
                            </ethernet-type>
                        </ethernet-match>
                        <arp-source-transport-address>{}</arp-source-transport-address>
                        <arp-target-transport-address>{}</arp-target-transport-address>
                    </match>
                </flow>
                """.format(out_port, flow_num, src_ip_addr, dst_ip_addr)
    return XML_Output

# Clearing flows directory
dir = 'Flows'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

# Creating First Switch Flows
XML_1_S1=flow_inport_outport(in_port=1,out_port=2,flow_num=1) # Port forwarding flow (refer to the function comment)
XML_2_S1=flow_inport_outport(in_port=2,out_port=1,flow_num=2)
# Writing the created flows as a .xml file
write_xml(XML_Data=XML_1_S1, Name_of_File='Flows/Switch1_Flow1')
write_xml(XML_Data=XML_2_S1, Name_of_File='Flows/Switch1_Flow2')

# Creating Second Switch Flows
XML_1_S2=flow_inport_outport(in_port=1,out_port=2,flow_num=1) # Port forwarding flow (refer to the function comment)
XML_2_S2=flow_inport_outport(in_port=2,out_port=1,flow_num=2)
# Writing the created flows as a .xml file
write_xml(XML_Data=XML_1_S2, Name_of_File='Flows/Switch2_Flow1')
write_xml(XML_Data=XML_2_S2, Name_of_File='Flows/Switch2_Flow2')

# Creating Router Flows
# ARP handling Flows
XML_ARP_1_R = flow_arp_L3(flow_num=1,src_ip_addr="10.0.1.1/32",dst_ip_addr="10.0.2.1/32",out_port=2) # Arp handling flow (refer to the function comment)
XML_ARP_2_R = flow_arp_L3(flow_num=2,src_ip_addr="10.0.2.1/32",dst_ip_addr="10.0.1.1/32",out_port=1)
# Writing the created flows as a .xml file
write_xml(XML_Data=XML_ARP_1_R, Name_of_File='Flows/Router_Flow1_ARP')
write_xml(XML_Data=XML_ARP_2_R, Name_of_File='Flows/Router_Flow2_ARP')
# IP handling Flows
XML_IP_1_R = flow_ip_L3(flow_num=3,src_ip_addr="10.0.1.1/32",dst_ip_addr="10.0.2.1/32",out_port=2) # IP forwarding flow (refer to the function comment)
XML_IP_2_R = flow_ip_L3(flow_num=4,src_ip_addr="10.0.2.1/32",dst_ip_addr="10.0.1.1/32",out_port=1)
# Writing the created flows as a .xml file
write_xml(XML_Data=XML_IP_1_R, Name_of_File='Flows/Router_Flow3_IP')
write_xml(XML_Data=XML_IP_2_R, Name_of_File='Flows/Router_Flow4_IP')
