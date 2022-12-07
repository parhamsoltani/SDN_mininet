import time
import requests
import copy from spf import *
from send_flows import *

# This function gets the link information from Delux App. To do so we send a "get" request to the controller (opendaylight-inventory).
def get_link_info(switch_id, eth_num):
    odl_url = """http://127.0.1.1:8080/restconf/operational/opendaylight-inventory:nodes/node/openflow:{}/node-connector/openflow:{}:{}""",format(switch_id, switch_id, eth_num)
    response = requests.get(odl_url, auth=("admin","admin"))
    return response

# This function uses the information obtained from the previous function.
def link_state(switch_id, eth_num):
    response=get_link_info(switch_id, eth_num)
    response_content=response.content
    if response_content.find('"link-down":false') != -1: # if there is a false state for the link-down in the message.
        link_state= "on"
    elif response_content.find('"link-down":true') != -1: # if there is a true state for the link-down in the message.
        link_state= "off"
    else:
        link_state="NO LINK"
    return link_state


# Reading the input weight matrix from a text file
with open('Weight_Mat.txt','r') as f:
    Weight_Mat = [[int(num) for num in line.split(',')] for line in f]

# This is an updated Weight Matrix after link changes.
Weight_Mat_Update=[copy.copy(x) for x in Weight_Mat]

# Initial path calculation and flow addition. So note that it is enough to ONLY run "watcher.py". It will add the initial flows itself.
# So there is no need to run "create_flows.py" and "send_flows.py" manually.
print("Initial Path Calcultaion:")
path1_new, path2_new = calculated_shortest_path_for_P4(Weigt_Mat_Update)
print("Initial Path From Switch 1 to Switch " + str(len(Weight_Mat_Update) + ": " + str([x+1 for x in path1_new]))
print("Initial Path From Switch " + str(len(Weight_Mat_Update)) + "to Switch 1: " + str([x+1 for x in path2_new]))
path2_new.reverse()

# Initial Path Flow Creation:
create_flows_for_P4(Weight_Mat_Update, path1_new, path2_new)
print("Initial flows saved in the 'Flow' directory.")
# Initial Path Flow Addition
send_flows_for_P4(Weight_Mat_Update)
print("Initial flows added to the switches. Now Switch 1 and Switch " + str(len(Weight_Mat_Update)) + "are connected on the mentioned paths. \n")
monitor_period=1
print("Monitoring State: Now we monitor link states every " + str(monitor_period) + " seconds. Please pay attention to the future logs.")
print("Monitor Period: Every " + str(monitor_period) + " Seconds \n")

# Monitoring State
rows, cols = (len(Weight_Mat_Update), len(Weight_Mat_Update))
link_stat=[["on"]*cols]*rows # At first all links assumed to be on

while 1:
    time.sleep(monitor_period)
    link_change= False
    path_change=""
    # Checking links states.
    for i in range(0, len(Weight_Mat)):
        if i==0:
            eth_count =1 # Because the first interface is for the host. So we have to add 1.
        else:
            eth_count=0
        for j in range(0, len(Weight_Mat)):
            if Weight_Mat[i][j] != 0 or Weight_Mat[j][i] != 0: # There is a link between these two switches.
                eth_count += 1
                if link_state(switch_id=i+1 , eth_num=eth_count) == "off" and link_stat[i][j] == "on" and j>i:
                    link_change = True
                    link_stat[i][j]="off"
                    path_change="Down"
                    Weight_Mat_Update[i][j]=0 # Making the link unavailable in the updated weight mat.
                    Weight_Mat_Update[j][i]=0
                    print("Link State Change: The link between switch " + str(i+1) + " and switch " + str(j+1) + " is DOWN.")
                elif link_state(switch_id=i+1, eth_num=eth_count) == "on" and link_stat[i][j]=="off" and j>i: # The last statement is for preventing loop, For instance (1,3) , (3,1).
                    link_change= True
                    link_stat[i][j]="on"
                    path_change = "Up"
                    Weight_Mat_Update[i][j]=copy.copy(Weight_Mat[i][j]) # Bringing back the link weight after it is up again.
                    Weight_Mat_Update[j][i]=copy.copy(Weight_Mat[i][j])
                    print("Link State Change: The link between switch " +  str(i+1) + " and switch " + str(j+1) + " is UP again.")

        if link_change:
            # Saving the old paths before link changes
            path1_old = path1_new[:]
            path2_old = path2_new[:]
            # Calculating new paths after link changes
            path1_new, path2_new = calculated_shortest_path_for_P4(Weight_Mat_Update)
            path2_new.reverse()

            if path1_new == path1_old_ and path2_new == path2_old:
                # if the new paths did NOT change after topology changes, so there is no need to send new flows.
                print("No Changes in Paths")
                print("The changed link was NOT on the path between source and destination switches. So no new flow has been added and the previous paths still stand. \n")
            else:
                # The topology changes caused changes in the paths. So we need to update the flows.
                create_flows_for_P4(Weight_Mat, path1_new, path2_new)
                send_flows_for_P4(Weight_Mat)
                if path_change == "Up":
                    print("Changes in Paths: New better Path")
                    print("The link which is up again is on a better path. So we update the path and save and send new flows.")
                if path_change == "Down":
                    print("Changes in Paths: Previous Path is now disconnected")
                    print("The link which failed, was on the previous paths. So previous paths are disconnected now. New paths has been calculated and now flows has been saved and sent to switches.")
                print("New Path from Switch 1 to Switch " + str(len(Weight_Mat_Update)) + ": " + str([x+1 for x in path1_new]))
                path2_new_print = [copy.copy(x) for x in path2_new]
                path2_new_print.reverse()
                print("New Path from Switch " + str(len(Weight_Mat_Update)) + " to Switch 1: " + str([x+1 for x in path2_new_print]) + "\n")
