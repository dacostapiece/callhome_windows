import requests
import json
from config import raspberry_vpn_component_id, remote_ssh_server_component_id

#UPDATE INCIDENT FOR HUB VPN
def update_incident(api_token, page_id, incident_id, name, status, updated_at, body):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/{incident_id}"
    headers = {
        "Authorization": api_token
    }
    data = {
        "incident[name]": name,
        "incident[status]": status,
        "incident[updated_at]": updated_at,
        "incident[body]": body,
        f"incident[component_ids][]": [{raspberry_vpn_component_id}],
        f"incident[components][{raspberry_vpn_component_id}]": "operational"
    }
    response = requests.patch(url, headers=headers, data=data)

    # Save response to a file
    with open("update_incident.txt", "w") as file:
        file.write(response.text)

    print("Incident updated. Response saved to update_incident.txt")
    response_data = response.json()
    solved_incident_id = response_data.get('id', None)
    print("solved incident: ", solved_incident_id)
    return solved_incident_id

#UPDATE INCIDENT FOR SSH SERVER CONNECTION
def update_incident_ssh(api_token, page_id, incident_id, name, status, updated_at, body):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/{incident_id}"
    headers = {
        "Authorization": api_token
    }
    data = {
        "incident[name]": name,
        "incident[status]": status,
        "incident[updated_at]": updated_at,
        "incident[body]": body,
        f"incident[component_ids][]": [{remote_ssh_server_component_id}],
        f"incident[components][{remote_ssh_server_component_id}]": "operational"
    }
    response = requests.patch(url, headers=headers, data=data)

    # Save response to a file
    with open("update_incident_ssh.txt", "w") as file:
        file.write(response.text)

    print("Incident updated. Response saved to update_incident_ssh.txt")
    response_data = response.json()
    solved_incident_id = response_data.get('id', None)
    print("solved incident: ", solved_incident_id)
    return solved_incident_id