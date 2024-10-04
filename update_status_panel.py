#!/usr/bin/env python3
from tunnel_connection import check_vpn_connection, check_ssh_connection
from check_incident_status import list_incident, raw_list_incident, list_incident_ssh, raw_list_incident_ssh
from config import api_token, page_id, name_create_incident, status_create_incident, impact_create_incident, monitoring_at_create_incident, body_create_incident, name_update_incident, status_update_incident, updated_at_update_incident, body_update_incident
from config import name_create_incident_ssh, status_create_incident_ssh, impact_create_incident_ssh, monitoring_at_create_incident_ssh, body_create_incident_ssh, name_update_incident_ssh, status_update_incident_ssh, updated_at_update_incident_ssh, body_update_incident_ssh
from create_incident_vpn import create_incident, create_incident_ssh
from update_incident_vpn import update_incident, update_incident_ssh

def is_vpn_working():
    if check_vpn_connection()==True:
        print("Checking if there any current Incidents?")
        if list_incident(api_token, page_id)==False:
            print("VPN is working, No related incidents found, OK!")
            return True
        else:
            current_incident_pair = raw_list_incident(api_token, page_id)
            print("Current Incident ID: ", current_incident_pair)
            print("VPN is working. Solving issue: ", current_incident_pair)
            for incident in current_incident_pair:
                solved_incident_id = update_incident(api_token, page_id, incident, name_update_incident, status_update_incident, updated_at_update_incident, body_update_incident)
            return solved_incident_id
    else:
        print("Checking if there any current Incidents?")
        if list_incident(api_token, page_id)==False:
            current_incident_pair = create_incident(api_token, page_id, name_create_incident, status_create_incident, impact_create_incident, monitoring_at_create_incident, body_create_incident)
            print("Created Incident ID: ", current_incident_pair)
            return current_incident_pair
        else:
            print("VPN is not working, But we´ve found registered incident, OK!")
            current_incident_pair = raw_list_incident(api_token, page_id)
            print("Ongoing Incident ID: ", current_incident_pair)
            return True    

print("Checking VPN Status...")
status_vpn = is_vpn_working()

def is_ssh_working():
    if check_ssh_connection()==True:
        print("Checking if there any current Incidents?")
        if list_incident_ssh(api_token, page_id)==False:
            print("SSH Server is working, No related incidents found, OK!")
            return True
        else:
            current_incident_pair = raw_list_incident_ssh(api_token, page_id)
            print("Current Incident ID: ", current_incident_pair)
            print("SSH Server is working. Solving issue: ", current_incident_pair)
            for incident in current_incident_pair:
                solved_incident_id = update_incident_ssh(api_token, page_id, incident, name_update_incident_ssh, status_update_incident_ssh, updated_at_update_incident_ssh, body_update_incident_ssh)
            return solved_incident_id
    else:
        print("Checking if there any current Incidents?")
        if list_incident_ssh(api_token, page_id)==False:
            current_incident_pair = create_incident_ssh(api_token, page_id, name_create_incident_ssh, status_create_incident_ssh, impact_create_incident_ssh, monitoring_at_create_incident_ssh, body_create_incident_ssh)
            print("Created Incident ID for SSH Server: ", current_incident_pair)
            return current_incident_pair
        else:
            print("SSH Server is not working, But we´ve found registered incident, OK!")
            current_incident_pair = raw_list_incident_ssh(api_token, page_id)
            print("Ongoing Incident ID for SSH Server: ", current_incident_pair)
            return True    

print("Checking SSH Server Status...")
status_ssh = is_ssh_working()