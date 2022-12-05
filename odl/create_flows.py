import os

# This function writes generated flow as a .xml file.
def write_xml(XML_Data, Name_of_File):
    with open(str(Name_of_File)+".xml",'wt') as f:
        f.write(XML_Data)
    f.close()

def flow_set_tun_id(in_port, flow_num, table_id, table_des, tun_id):
    XML_Output = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <flow xmlns="urn:opendaylight:flow:inventory">
                    <strict>false</strict>
                    <instructions>
                        <instruction>
                            <order>0</order>
                            <apply-actions>
                                <action>
                                    <order>0</order>
                                    <set-field>
                                        <tunnel>
                                            <tunnel-id>{}</tunnel-id>
                                        </tunnel>
                                    </set-field>
                                </action>
                            </apply-actions>
                        </instruction>
                        <instruction>
                            <order>1</order>
                            <go-to-table>
                                <table-id>{}</table-id>
                            </go-to-table>
                        </instruction>
                    </instructions>
                    <table-id>{}</table-id>
                    <id>{}</id>
                    <match>
                        <in-port>{}</in-port>
                    </match>
                </flow>
                """.format(tun_id, table_des, table_id, flow_num, in_port)
    return XML_Output


def flow_go_to_table(flow_num, table_id, table_des):
    XML_Output = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <flow xmlns="urn:opendaylight:flow:inventory">
                    <strict>false</strict>
                    <instructions>
                        <instruction>
                            <order>1</order>
                            <go-to-table>
                                <table-id>{}</table-id>
                            </go-to-table>
                        </instruction>
                    </instructions>
                    <table-id>{}</table-id>
                    <id>{}</id>
                </flow>
                """.format(table_des, table_id, flow_num)
    return XML_Output

def flow_tun_dl_dst(out_port, table_id, flow_num, tun_id, dl_dst):
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
                    <id>{}</id>
                    <table-id>{}</table-id>
                    <match>
                        <ethernet-match>
                            <ethernet-destination>
                                <address>{}</address>
                            </ethernet-destination>
                        </ethernet-match>
                        <tunnel>
                            <tunnel-id>{}</tunnel-id>
                        </tunnel>
                    </match>
                </flow>
                """.format(out_port, flow_num, table_id, dl_dst, tun_id)
    return XML_Output

def flow_drop_priority(priority, table_id, flow_num):
    XML_Output = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <flow xmlns="urn:opendaylight:flow:inventory">
                    <strict>false</strict>
                    <instructions>
                        <instruction>
                            <order>0</order>
                            <apply-actions>
                                <action>
                                    <order>0</order>
                                    <drop-action/>
                                </action>
                            </apply-actions>
                        </instruction>
                    </instructions>
                    <id>{}</id>
                    <table-id>{}</table-id>
                    <priority>{}</priority>
                </flow>
                """.format(flow_num, table_id, priority)
    return XML_Output

# This function forward Arp packets. So this function handles arps.
def flow_arp_L3(out_port, table_id, flow_num, des_ip_addr, tun_id):
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
                    <table-id>{}</table-id>
                    <id>{}</id>
                    <match>
                        <ethernet-match>
                            <ethernet-type>
                                <type>2054</type>
                            </ethernet-type>
                        </ethernet-match>
                        <arp-target-transport-address>{}</arp-target-transport-address>
                        <tunnel>
                            <tunnel-id>{}</tunnel-id>
                        </tunnel>
                    </match>
                </flow>
                """.format(out_port, table_id, flow_num, des_ip_addr, tun_id)
    return XML_Output

# Clearing Flows Directory
dir = 'Flows'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

# Creating First Switch Flows (which is on VM1)
XML_1_S1 = flow_set_tun_id(in_port=1, flow_num=1, table_id=0, table_des=1, tun_id=100)
XML_2_S1 = flow_set_tun_id(in_port=2, flow_num=2, table_id=0, table_des=1, tun_id=200)
XML_3_S1 = flow_go_to_table(flow_num=3, table_id=0, table_des=1)

XML_4_S1 = flow_tun_dl_dst(out_port=1, table_id=1, flow_num=4, tun_id=100, dl_dst="00:00:00:00:00:01")
XML_5_S1 = flow_tun_dl_dst(out_port=2, table_id=1, flow_num=5, tun_id=200, dl_dst="00:00:00:00:00:01")
XML_6_S1 = flow_tun_dl_dst(out_port=9, table_id=1, flow_num=6, tun_id=100, dl_dst="00:00:00:00:00:02")
XML_7_S1 = flow_tun_dl_dst(out_port=9, table_id=1, flow_num=7, tun_id=200, dl_dst="00:00:00:00:00:02")

XML_8_S1 = flow_arp_L3(out_port=1, table_id=1, flow_num=8, des_ip_addr="10.0.0.1/32", tun_id=100)
XML_9_S1 = flow_arp_L3(out_port=2, table_id=1, flow_num=9, des_ip_addr="10.0.0.1/32", tun_id=200)
XML_10_S1 = flow_arp_L3(out_port=9, table_id=1, flow_num=10, des_ip_addr="10.0.0.2/32", tun_id=100)
XML_11_S1 = flow_arp_L3(out_port=9, table_id=1, flow_num=11, des_ip_addr="10.0.0.2/32", tun_id=200)

XML_12_S1 = flow_drop_priority(priority=100, table_id=1, flow_num=12)

# Writing the created flows as a .xml file
write_xml(XML_Data=XML_1_S1, Name_of_File='Flows/Switch1_Flow1')
write_xml(XML_Data=XML_2_S1, Name_of_File='Flows/Switch1_Flow2')
write_xml(XML_Data=XML_3_S1, Name_of_File='Flows/Switch1_Flow3')
write_xml(XML_Data=XML_4_S1, Name_of_File='Flows/Switch1_Flow4')
write_xml(XML_Data=XML_5_S1, Name_of_File='Flows/Switch1_Flow5')
write_xml(XML_Data=XML_6_S1, Name_of_File='Flows/Switch1_Flow6')
write_xml(XML_Data=XML_7_S1, Name_of_File='Flows/Switch1_Flow7')
write_xml(XML_Data=XML_8_S1, Name_of_File='Flows/Switch1_Flow8')
write_xml(XML_Data=XML_9_S1, Name_of_File='Flows/Switch1_Flow9')
write_xml(XML_Data=XML_10_S1, Name_of_File='Flows/Switch1_Flow10')
write_xml(XML_Data=XML_11_S1, Name_of_File='Flows/Switch1_Flow11')
write_xml(XML_Data=XML_12_S1, Name_of_File='Flows/Switch1_Flow12')

# Creating Second Switch Flows (Which is on VM2)
XML_1_S2 = flow_set_tun_id(in_port=1, flow_num=1, table_id=0, table_des=1, tun_id=100)
XML_2_S2 = flow_set_tun_id(in_port=2, flow_num=2, table_id=0, table_des=1, tun_id=200)
XML_3_S2 = flow_go_to_table(flow_num=3, table_id=0, table_des=1)

XML_4_S2 = flow_tun_dl_dst(out_port=1, table_id=1, flow_num=4, tun_id=100, dl_dst="00:00:00:00:00:02")
XML_5_S2 = flow_tun_dl_dst(out_port=2, table_id=1, flow_num=5, tun_id=200, dl_dst="00:00:00:00:00:02")
XML_6_S2 = flow_tun_dl_dst(out_port=9, table_id=1, flow_num=6, tun_id=100, dl_dst="00:00:00:00:00:01")
XML_7_S2 = flow_tun_dl_dst(out_port=9, table_id=1, flow_num=7, tun_id=200, dl_dst="00:00:00:00:00:01")

XML_8_S2 = flow_arp_L3(out_port=9, table_id=1, flow_num=8, des_ip_addr="10.0.0.1/32", tun_id=100)
XML_9_S2 = flow_arp_L3(out_port=9, table_id=1, flow_num=9, des_ip_addr="10.0.0.1/32", tun_id=200)
XML_10_S2 = flow_arp_L3(out_port=1, table_id=1, flow_num=10, des_ip_addr="10.0.0.2/32", tun_id=100)
XML_11_S2 = flow_arp_L3(out_port=2, table_id=1, flow_num=11, des_ip_addr="10.0.0.2/32", tun_id=200)

XML_12_S2 = flow_drop_priority(priority=100, table_id=1, flow_num=12)

# Writing the created flows as a .xml file
write_xml(XML_Data=XML_1_S2, Name_of_File='Flows/Switch1_Flow1')
write_xml(XML_Data=XML_2_S2, Name_of_File='Flows/Switch1_Flow2')
write_xml(XML_Data=XML_3_S2, Name_of_File='Flows/Switch1_Flow3')
write_xml(XML_Data=XML_4_S2, Name_of_File='Flows/Switch1_Flow4')
write_xml(XML_Data=XML_5_S2, Name_of_File='Flows/Switch1_Flow5')
write_xml(XML_Data=XML_6_S2, Name_of_File='Flows/Switch1_Flow6')
write_xml(XML_Data=XML_7_S2, Name_of_File='Flows/Switch1_Flow7')
write_xml(XML_Data=XML_8_S2, Name_of_File='Flows/Switch1_Flow8')
write_xml(XML_Data=XML_9_S2, Name_of_File='Flows/Switch1_Flow9')
write_xml(XML_Data=XML_10_S2, Name_of_File='Flows/Switch1_Flow10')
write_xml(XML_Data=XML_11_S2, Name_of_File='Flows/Switch1_Flow11')
write_xml(XML_Data=XML_12_S2, Name_of_File='Flows/Switch1_Flow12')
