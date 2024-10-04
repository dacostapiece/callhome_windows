#!/usr/bin/env python3
import requests
import ipaddress
import subprocess
import re
from datetime import datetime
from config import ZONE_ID, DNS_RECORD_ID, DNS_RECORD_NAME, CF_API_TOKEN

LOG_FILE_PATH = "/tmp/update_tun0_ipname.log"

def log_run_time():
    """Logs the date and time the script was run to the log file."""
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write("\n")
        log_file.write(f"Script run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Function to get the IP address from interface tun0
def get_tun0_ip():
    try:
        # Run the Linux command to get the IP address of the tun0 interface
        output = subprocess.check_output(["ip", "addr", "show", "tun0"]).decode("utf-8")
        # Use regular expression to extract the IP address
        tun0_ip = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output).group(1)
        return tun0_ip
    except subprocess.CalledProcessError:
        print("Interface tun0 not found.")
        return None


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

def main():
    tun0_ip = get_tun0_ip()
    log_run_time()  # Fixed indentation here
    if tun0_ip:
        update_dns_record(tun0_ip)

if __name__ == "__main__":
    main()
