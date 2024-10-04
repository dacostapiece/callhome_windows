import requests
from datetime import datetime
from config import raspberry_vpn_component_id, remote_ssh_server_component_id

#CREATE INCIDENT FOR RASPBERRY TO HUB VPN CONNECTION
def create_incident(api_token, page_id, name, status, impact, monitoring_at, body):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents"
    headers = {
        "Authorization": f"OAuth {api_token}"
    }
    data = {
        "incident[name]": name,
        "incident[status]": status,
        "incident[impact]": impact,
        "incident[monitoring_at]": monitoring_at,
        "incident[body]": body,
        f"incident[component_ids][]": [{raspberry_vpn_component_id}],
        f"incident[components][{raspberry_vpn_component_id}]": "partial_outage"
    }
    response = requests.post(url, headers=headers, data=data)

    # Save response to a file
    with open("create_incident_response.txt", "w") as file:
        file.write(response.text)

    print("An incident has been created.")
    print("Response saved to create_incident_response.txt")
    response_data = response.json()

    # Extract incident ID and component IDs
    incident_id = response_data.get('id', None) if response_data else None
    component_ids = [component.get('id') for component in response_data.get('components', [])]

    if component_ids:
        component_ids_isolated = component_ids[0]
    else:
        component_ids_isolated=None

    # Print the results
    print(f"Incident ID: {incident_id}")
    print(f"Component IDs: {component_ids_isolated}")

    print("Pair Incident")
    pair_incident = [incident_id, component_ids_isolated]
    print(pair_incident)

    # Save Pair Incident to a file
    print("Response saved to create_pair_incident_response_vpn.txt")
    with open("create_pair_incident_response_vpn.txt", "w") as file:
        file.write(str(pair_incident))
    
    return pair_incident

#CREATE INCIDENT FOR RASPBERRY TO SSH SERVER CONNECTION
def create_incident_ssh(api_token, page_id, name, status, impact, monitoring_at, body):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents"
    headers = {
        "Authorization": f"OAuth {api_token}"
    }
    data = {
        "incident[name]": name,
        "incident[status]": status,
        "incident[impact]": impact,
        "incident[monitoring_at]": monitoring_at,
        "incident[body]": body,
        f"incident[component_ids][]": [{remote_ssh_server_component_id}],
        f"incident[components][{remote_ssh_server_component_id}]": "partial_outage"
    }
    response = requests.post(url, headers=headers, data=data)

    # Save response to a file
    with open("create_incident_response_ssh.txt", "w") as file:
        file.write(response.text)

    print("An incident has been created.")
    print("Response saved to create_incident_response_ssh.txt")
    response_data = response.json()

    # Extract incident ID and component IDs
    incident_id = response_data.get('id', None) if response_data else None
    component_ids = [component.get('id') for component in response_data.get('components', [])]

    if component_ids:
        component_ids_isolated = component_ids[0]
    else:
        component_ids_isolated=None

    # Print the results
    print(f"Incident ID: {incident_id}")
    print(f"Component IDs: {component_ids_isolated}")

    print("Pair Incident")
    pair_incident = [incident_id, component_ids_isolated]
    print(pair_incident)

    # Save Pair Incident to a file
    print("Response saved to create_pair_incident_response_ssh.txt")
    with open("create_pair_incident_response_ssh.txt", "w") as file:
        file.write(str(pair_incident))
    
    return pair_incident