import requests
from requests.auth import HTTPBasicAuth

#this func deletes all the flows in the input switch
def delete_flow(switch_id,tabel_id):
    odl_url="""http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{}/table/{}""".format(switch_id,table_id)
    headers={'Content-Type':'application/xml'}
    requests.delete(odl_url,headers=headers,auth=("admin","admin"))

#this func reads the flow from the .xml file put it to the controller using 'requests' function
#after calling this function the real flow will be added to the switch
def put_flow(switch_id,flow_num,flow_name):
    odl_url="""http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{}/table/0/{}""".format(switch_id,flow_num)
    headers={'Content-Type':'application/yang.data+xml'}
    dataXML=open(flow_name + ".xml",'r')
    requests.put(odl_url,data=dataXML,headers=headers,auth=("admin","admin"))

#cleaning the switch from previous flows
for tb_id in range(0,10):
    delete_flow(switch_id=11,table_id=tb_id)
    
#adding flows to the first switch
put_flow(switch_id=11,flow_num=1,flow_name="Flows/Switch1_Flow1")
put_flow(switch_id=11,flow_num=2,flow_name="Flows/Switch1_Flow2")

#adding flows to the second switch
for tb_id in range(0,10):
    delete_flow(switch_id=13,table_id=tb_id)
put_flow(switch_id=13,flow_num=1,flow_name="Flows/Switch2_Flow1")
put_flow(switch_id=13,flow_num=2,flow_name="Flows/Switch2_Flow2")

#adding flows to the router
for tb_id in range(0,10):
    delete_flow(switch_id=12,table_id=tb_id)
put_flow(switch_id=12,flow_num=1,flow_name="Flows/Router_Flow1_ARP")
put_flow(switch_id=12,flow_num=2,flow_name="Flows/Router_Flow2_ARP")
put_flow(switch_id=12,flow_num=3,flow_name="Flows/Router_Flow3_IP")
put_flow(switch_id=12,flow_num=4,flow_name="Flows/Router_Flow4_IP")
