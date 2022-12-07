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

def create_flows_for_P4(Weight_Mat, path1_new, path2_new):
    # Clearing Flows Directory
    dir = 'Flows'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir,f))

    path1=path1_new
    path2=path2_new

    # Making flows for ARP and IP handling for all of the switches in Path1 (Node 1 to n)
    path=path1
    for index in range(0, len(path)):
        if index == 0: # First Switch in the path which is connected to first host.
            interface_num = 0
            for col in range(0, path[index +1] +1): # Here we calculate what is the interface number of the switch which connects it to the next switch in the path.
                if Weight_Mat[path[[index]][col] !=0 or Weight_Mat[col][path[index]] != 0: # if the node is connected to other node or if another node is connected to it.
                    # Note that one way link is also an interface in the other switch. But we are aware of that and do not use the other direction at all.
                    interface_num = interface_num +1
            interface_num = interface_num + 1 # Because the first interface is for the host. So we have to shift for one interface.

            XML_S1_F1 = Flow_arp_L3(flow_num=1, src_ip_addr="10.0.1.1/32", dst_ip_addr="10.0.2.1/32", out_port=interface_num) # Connecting the first host to the next switch in the path for ARP handling.
            XML_S1_F2 = Flow_ip_L3(flow_num=2, src_ip_addr="10.0.1.1/32", dst_ip_addr="10.0.2.1/32", out_port=interface_num) # Connecting the first host to the next switch in the path for IP handling.
            write_xml(XML_Data=XML_S1_F1, Name_of_File='Flows/S' + str(path[index] + 1) + '_F1')
            write_xml(XML_Data=XML_S1_F2, Name_of_File='Flows/S' + str(path[index] + 1) + '_F2')
        elif index == len(path) -1: # Last Switch in the path which is connected to second host.
            host_interface_num = 0

            for col in range(0, len(Weight_Mat)): # Here we calculate what is the interface number of the switch which connects it to the host.
                if Weight_Mat[path[index]][col] != 0 or Weight_Mat[col][path[index]] != 0:
                    host_interface_num = host_interface_num + 1
            host_interface_num = host_interface_num + 1
            XML_SN_F1 = flow_arp_L3(flow_num=1, src_ip_addr="10.0.1.1/32", dst_ip_addr="10.0.2.1/32", out_port=host_interface_num) # Connecting the last switch in the path to the second host for ARP handling.
            XML_SN_F2 = flow_arp_L3(flow_num=2, src_ip_addr="10.0.1.1/32", dst_ip_addr="10.0.2.1/32", out_port=host_interface_num) # Connecting the last switch in the path to the second host for IP handling.
            write_xml(XML_Data=XML_SN_F1, Name_of_File='Flows/S' + str(path[index] + 1) + '_F1')
            write_xml(XML_Data=XML_SN_F2, Name_of_File='Flows/S' + str(path[index] + 1) + '_F2')

        else: #Switches in the path which are between first and last switches
            interface_out=0
            for col in range(0, path[index +1]+1): # Here we calculate what is the interface number of the switch which connects it to the next switch in the path.
                if Weight_Mat[path[index]][col] != 0 or Weight_Mat[col][path[index]] != 0:
                    interface_out = interface_out +1
            XML_SB_F1 = flow_arp_L3(flow_num=1, src_ip_addr="10.0.1.1/32", dst_ip_addr="10.0.2.1/32", out_port=interface_out) # Connecting switch to the next switch in the path for ARP handling.
            XML_SB_F2 = flow_arp_L3(flow_num=2, src_ip_addr="10.0.1.1/32", dst_ip_addr="10.0.2.1/32", out_port=interface_out) # Connecting switch to the previous switch in the path for IP handling.
            write_xml(XML_Data=XML_SB_F1, Name_of_File='Flows/S' + str(path[index] + 1) + '_F1')
            write_xml(XML_Data=XML_SB_F2, Name_of_File='Flows/S' + str(path[index] + 1) + '_F2')


    # Making Flows for ARP and IP handling for all of the switches in Path2 (Node n to 1)
    path = path2
    for index in range(0, len(path)):
        if index == 0: # First Switch in the path which is connected to first host.
            XML_S1_F3 = flow_arp_L3(flow_num=3, src_ip_addr="10.0.2.1/32", dst_ip_addr="10.0.1.1/32", out_port=1) # Connecting the first switch to the first host for ARP handling.
            XML_S1_F4 = flow_ip_L3(flow_num=4, src_ip_addr="10.0.2.1/32", dst_ip_addr="10.0.1.1/32", out_port=1) # Connecting the first switch to the first host for IP handling.
            write_xml(XML_Data=XML_S1_F3, Name_of_File='Flows/S' + str(path[index] + 1) + '_F3')
            write_xml(XML_Data=XML_S1_F4, Name_of_File='Flows/S' + str(path[index] + 1) + '_F4')
        elif index == len(path) - 1: # Last Switch in the path which is connected to second host.
            pre_interface_num=0
            for col in range(0, path[index-1]+1): #Here we calculate what is the interface number of the switch which connects it to the previous switch in the path.
                if Weight_Mat[path[index]][col] !=0 or Weight_Mat[col][path[index]] !=0 :
                    pre_interface_num = pre_interface_num + 1
            XML_SN_F3 = flow_arp_L3(flow_num=1, src_ip_addr="10.0.2.1/32", dst_ip_addr="10.0.2.1/32", out_port=pre_interface_num) # Connects the last switch in the path to the previous switch.
            XML_SN_F4 = flow_arp_L3(flow_num=2, src_ip_addr="10.0.2.1/32", dst_ip_addr="10.0.2.1/32", out_port=pre_interface_num) # Connects the last switch in the path to the previous switch.
            write_xml(XML_Data=XML_SN_F3, Name_of_File='Flows/S' + str(path[index] + 1) + '_F3')
            write_xml(XML_Data=XML_SN_F4, Name_of_File='Flows/S' + str(path[index] + 1) + '_F4')   
        else: #Switches in the path which are between first and last switches
            interface_out=0
            for col in range(0, path[index - 1]+1): # Here we calculate what is the interface number of the switch which connects it to the next switch in the path.
                if Weight_Mat[path[index]][col] != 0 or Weight_Mat[col][path[index]] != 0:
                    interface_out = interface_out +1
            XML_SB_F3 = flow_arp_L3(flow_num=3, src_ip_addr="10.0.2.1/32", dst_ip_addr="10.0.1.1/32", out_port=interface_out) # Connecting switch to the next switch in the path for ARP handling.
            XML_SB_F4 = flow_arp_L3(flow_num=4, src_ip_addr="10.0.2.1/32", dst_ip_addr="10.0.1.1/32", out_port=interface_out) # Connecting switch to the previous switch in the path for IP handling.
            write_xml(XML_Data=XML_SB_F3, Name_of_File='Flows/S' + str(path[index] + 1) + '_F3')
            write_xml(XML_Data=XML_SB_F4, Name_of_File='Flows/S' + str(path[index] + 1) + '_F4')
