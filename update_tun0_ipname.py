#!/usr/bin/env python3
import os
import requests
import ipaddress
import subprocess
import re
from datetime import datetime
from config import ZONE_ID, DNS_RECORD_ID, DNS_RECORD_NAME, CF_API_TOKEN, home_dir
from myip_windows import get_network_interfaces 
import pdb

# Define the log file path for Windows
LOG_FILE_PATH = os.path.join(os.getcwd(), os.path.join(home_dir, "logs"), "update_tun0_ipname.log")

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

def log_run_time():
    """Logs the date and time the script was run to the log file."""
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write("\n")
        log_file.write(f"Script run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Function to update DNS record in Cloudflare
def update_dns_record(ip):
    headers = {
        'Authorization': f'Bearer {CF_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records'
    params = {
        'type': 'A',
        'name': DNS_RECORD_NAME
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if response.status_code == 200 and data['success']:
        record_id = data['result'][0]['id']
        update_url = f'{url}/{record_id}'
        payload = {
            'type': 'A',
            'name': DNS_RECORD_NAME,
            'id': record_id,
            'content': ip,
            'ttl': 120,  # Adjust TTL as needed
            'proxied': False  # Adjust proxy settings as needed
        }
        response = requests.put(update_url, headers=headers, json=payload)
        if response.status_code == 200 and response.json()['success']:
            print(f"DNS record {DNS_RECORD_NAME} updated successfully with IP address {ip}.")
            with open(LOG_FILE_PATH, 'a') as log_file:
                log_file.write(f"DNS record {DNS_RECORD_NAME} updated successfully with IP address {ip}.\n")
        else:
            print("Failed to update DNS record.")
            with open(LOG_FILE_PATH, 'a') as log_file:
                log_file.write(f"Failed to update DNS record.\n")
    else:
        print("Failed to fetch DNS record ID.")
        print(response.content)  # Print response content for debugging
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"Failed to fetch DNS record ID.\n")

tun0_ip = get_network_interfaces()
log_run_time()  # Fixed indentation here
#pdb.set_trace()
if tun0_ip:
    update_dns_record(tun0_ip)