import requests
from config import raspberry_vpn_component_id, remote_ssh_server_component_id

#HUB VPN INCIDENT
def list_incident(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    # Save response to a file
    with open("check_incident_status_response.txt", "w") as file:
        file.write(response.text)
        print("Response saved to check_incident_status_response.txt")

    if not response_data:
        print("No incidents found.")
        return False
    
    # Extract incident ID and component IDs
    related_incidents = []  # List to store all related incidents
    
    if not response_data:
        print("No incidents found.")
        return related_incidents

    print("Check Incident Association")
    loop_number = 1
    for incident in response_data:

        # Get the incident ID
        incident_id = incident.get('id', None)
        
        # Get the component IDs associated with this incident
        component_ids = [component.get('id') for component in incident.get('components', [])]

        # Isolate the first component ID if it exists
        component_ids_isolated = component_ids[0] if component_ids else None

        # Pair the incident ID with the isolated component ID
        pair_incident = [incident_id, component_ids_isolated]

        # Check if the incident is related to Rasp VPN
        if pair_incident[1] == raspberry_vpn_component_id:
            print(f"Incident ID {pair_incident[0]} is related to Rasp VPN.")
            #pdb.set_trace()  # Set a breakpoint
            related_incidents.append(pair_incident[0])
            loop_number+=1
        else:
            print(f"Incident ID {pair_incident[0]} is not related to Rasp VPN.")
            #pdb.set_trace()  # Set a breakpoint
            loop_number+=1

    if not related_incidents:
        print("No unresolved incidents found for Rasp VPN.")       
        return False

    print("VPN Related Incidents:", related_incidents)

    return related_incidents

def raw_list_incident(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    #Extract incident ID and component IDs
    related_incidents = []  # List to store all related incidents

    loop_number = 1
    for incident in response_data:

        # Get the incident ID
        incident_id = incident.get('id', None)
        
        # Get the component IDs associated with this incident
        component_ids = [component.get('id') for component in incident.get('components', [])]

        # Isolate the first component ID if it exists
        component_ids_isolated = component_ids[0] if component_ids else None

        # Pair the incident ID with the isolated component ID
        pair_incident = [incident_id, component_ids_isolated]
        
        # Check if the incident is related to Rasp VPN
        if pair_incident[1] == raspberry_vpn_component_id:
            print(f"Incident ID {pair_incident[0]} is related to Rasp VPN.")
            related_incidents.append(pair_incident[0])
            loop_number+=1
        else:
            print(f"Incident ID {pair_incident[0]} is not related to Rasp VPN.")

            loop_number+=1

    if not related_incidents:
        print("No unresolved incidents found for Rasp VPN.")       
        return False

    print("Raw VPN Related Incidents:", related_incidents)

    return related_incidents
    
    #SSH SERVER INCIDENT
def list_incident_ssh(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    # Save response to a file
    with open("check_incident_status_response_ssh.txt", "w") as file:
        file.write(response.text)
        print("Response saved to check_incident_status_response_ssh.txt")

    if not response_data:
        print("No incidents found.")
        return False
    
    # Extract incident ID and component ID
    related_incidents = []  # List to store all related incidents

    if not response_data:
        print("No incidents found.")
        return related_incidents

    loop_number = 1
    for incident in response_data:

        # Get the incident ID
        incident_id = incident.get('id', None)
        
        # Get the component IDs associated with this incident
        component_ids = [component.get('id') for component in incident.get('components', [])]

        # Isolate the first component ID if it exists
        component_ids_isolated = component_ids[0] if component_ids else None

        # Pair the incident ID with the isolated component ID
        pair_incident = [incident_id, component_ids_isolated]

        # Check if the incident is related to Rasp VPN
        if pair_incident[1] == remote_ssh_server_component_id:
            print(f"Incident ID {pair_incident[0]} is related to Remote SSH Server.")
            related_incidents.append(pair_incident[0])
            loop_number+=1
        else:
            print(f"Incident ID {pair_incident[0]} is not related to Remote SSH Server.")
            loop_number+=1

    if not related_incidents:
        print("No unresolved incidents found for Remote SSH Server.")       
        return False

    print("SSH Related Incidents:", related_incidents)

    return related_incidents


def raw_list_incident_ssh(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    #Extract incident ID and component IDs
    related_incidents = []  # List to store all related incidents

    loop_number = 1
    for incident in response_data:

        # Get the incident ID
        incident_id = incident.get('id', None)
        
        # Get the component IDs associated with this incident
        component_ids = [component.get('id') for component in incident.get('components', [])]

        # Isolate the first component ID if it exists
        component_ids_isolated = component_ids[0] if component_ids else None

        # Pair the incident ID with the isolated component ID
        pair_incident = [incident_id, component_ids_isolated]

        # Check if the incident is related to Rasp VPN
        if pair_incident[1] == remote_ssh_server_component_id:
            print(f"Incident ID {pair_incident[0]} is related to Remote SSH Server.")
            related_incidents.append(pair_incident[0])
            loop_number+=1
        else:
            print(f"Incident ID {pair_incident[0]} is not related to Remote SSH Server.")
            loop_number+=1

    if not related_incidents:
        print("No unresolved incidents found for Remote SSH Server.")       
        return False

    print("Raw SSH Related Incidents:", related_incidents)

    return related_incidents
