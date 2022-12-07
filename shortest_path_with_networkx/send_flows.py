import requests
from requests.auth import HTTPBasicAuth
import os.path
from spf import *

# This function deletes all the flows in the input switch.
def delete_flow(switch_id, table_id):
    odl_url="""http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{}/table/{}""".format(switch_id, table_id)
    headers = {'Content-Type':'application/xml'}
    requests.delete(odl_url, headers=headers, auth=("admin","admin"))

# This function reads the flow from the .xml file and put it to the controller using "requests" function.
# After calling this function, the read flow will be added to the switch.
def put_flow(switch_id, flow_num, flow_name):
    odl_url="""http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{}/table/0/flow/{}""".format(switch_id, flow_num)
    headers = {'Content-Type':'application/yang.data+xml'}
    dataXML = open(flow_name + ".xml", "r")
    requests.put(odl_url, data=dataXML, headers=headers, auth=("admin","admin"))

# Sending previously made flows to the switches in the path. Each flow has a name Si_Fj, which means the j'th flow of the i'th switch.
# i'th switch means the i'th in the path, not the i'th defined switch

def send_flows_for_P4(Weight_Mat):
    for index in range(0, len(Weight_Mat)):
        # First we clean the switch from previous flows.
        for tb_id in range(0,10):
            delete_flows(switch_id=index+1, table_id=tb_id)
        if os.path.exists('Flows/S' + str(index+1) + '_F1.xml'):
            put_flow(switch_id=index+1, flow_num=1, flow_name='Flow/S' + str(index +1) + '_F1')
        if os.path.exists('Flows/S' + str(index+1) + '_F2.xml'):
            put_flow(switch_id=index+1, flow_num=2, flow_name='Flow/S' + str(index +1) + '_F2')
        if os.path.exists('Flows/S' + str(index+1) + '_F3.xml'):
            put_flow(switch_id=index+1, flow_num=3, flow_name='Flow/S' + str(index +1) + '_F3')
        if os.path.exists('Flows/S' + str(index+1) + '_F4.xml'):
            put_flow(switch_id=index+1, flow_num=4, flow_name='Flow/S' + str(index +1) + '_F4')
            
