import subprocess
import time
from config import vpn_probe_target, ssh_server, ssh_port
import re
import socket
import sys
import logging
from ping3 import ping, errors
import os
from myip_windows import is_ipv4, is_apipa_or_loopback
import json

# Define the log file path for Windows
LOG_FILE_PATH = os.path.join(os.getcwd(), "logs", "tunnel_connection.log")

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

#HUB VPN CHECK
def check_tun0_ip():
    # PowerShell command to retrieve network interface, IP address, and adapter details
    command = """
    Get-NetAdapter | ForEach-Object {
        $adapter = $_
        Get-NetIPAddress -InterfaceAlias $adapter.Name | ForEach-Object {
            [PSCustomObject]@{
                ConnectionName = $adapter.Name
                AdapterName = $adapter.InterfaceDescription
                IPAddress = $_.IPAddress
            }
        }
    } | ConvertTo-Json
    """
    try:
        # Run the PowerShell command and capture the output
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        
        # Parse the JSON output into Python objects (list of dictionaries)
        interfaces = json.loads(result.stdout)
        
        tunnel_ipaddresses = []  # Use a list to store multiple tunnel IP addresses
        interface_count = 0
        
        # Iterate through interfaces and print the details
        for interface in interfaces:
            ip_address = interface.get("IPAddress")
            adapter_name = interface.get("AdapterName")
            connection_name = interface.get("ConnectionName")
            
            # Increment interface count for display
            interface_count += 1

            # Check if the adapter is TAP-Windows or TAP-Win32, and the IP is IPv4
            if ("TAP-Windows Adapter" in adapter_name or "TAP-Win32 Adapter" in adapter_name) and is_ipv4(ip_address):
                # Check if it's an APIPA (169.254.x.x) or loopback address (127.x.x.x)
                if not is_apipa_or_loopback(ip_address):  # Only add if it's not APIPA or loopback
                    tunnel_ipaddresses.append(ip_address)  # Append the valid tunnel IP address

        # If any tunnel IP addresses were found, print them
        if tunnel_ipaddresses:
            print("Tunnel IP Addresses:")
            for addr in tunnel_ipaddresses:
                print(f"  {addr}")
                return True
        else:
            print("No matching TAP-Windows Adapter with an IPv4 address found.")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return False

#PING3
def ping_ip(ip, timeout=10):
    #ip = "172.16.113.4"
    try:
        # Ensure the IP is a valid string before passing to ping
        if not isinstance(ip, str) or not ip:
            raise ValueError(f"Invalid IP address: {ip}")
        # Send ICMP request and get the response time
        print("\n")
        print("ping ip funcion")
        print("early")
        print("ip: ", ip)
        print("RESPONSE TIME BROTHER")
        #pdb.set_trace()
        response_time="Starting Response Time"
        print("response_time: ", response_time)
        #RUNNING IS BREAKING HERE


        response_time = ping(ip, timeout=timeout)
        print("RESPONSE TIME SISTER")
        print("later")
        print("ip: ", ip)
        print("response_time: ", response_time)

        if response_time is None:
            print(f"Ping to {ip} failed. No response.")
            time.sleep(1)
            return "Falseano brow"  # Return a proper boolean value
        else:
            print(f"Ping to {ip} successful. Response time: {response_time} seconds")
            return True

    except Exception as e:
        print(f"ICMP error occurred while pinging {ip}: {str(e)}")
        time.sleep(1)
        return False

    except ValueError as ve:
        print("ValueError")
        print(str(ve))
        return False

def check_vpn_connection():
    if check_tun0_ip():
        if ping_ip(vpn_probe_target):
            print("Remote probe ", vpn_probe_target, " is responding!")
            return True
        else:
            print("Dev tun0 has IP address, but remote target isn't replying")
            return False
    else:
        print("Dev tun0 doesnt exist - OpenVPN is not working at all")
        return False

#SSH SERVER CHECK    
def resolve_dns(hostname):
    """ Resolve DNS hostname to IP address or return if already an IP address. """
    # Regular expression to match IPv4 addresses
    ipv4_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    
    # Check if the hostname is an IPv4 address
    if ipv4_pattern.match(hostname):
        return hostname  # Return the IPv4 address as is
    
    # If not an IPv4 address, resolve the DNS hostname to an IP address
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror as e:
        print(f"Error resolving DNS in tunnel_connection for {hostname}: {e}")
        logging.error(f"Error resolving DNS in tunnel_connection for {hostname}: {e}")
        sys.exit(2)

def is_ssh_tunnel_active(host, port):
    """ Check if the SSH tunnel is active by attempting a connection. """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except socket.error:
        return False
    finally:
        s.close()

def check_ssh_connection():
    # Resolve DNS to get SSH server IP address
    ssh_server_ip = resolve_dns(ssh_server)

    # Open the log file for writing (append mode to keep all output)
    LOG_FILE_PATH

     # Check if the SSH server is reachable before starting autossh
    if is_ssh_tunnel_active(ssh_server_ip, ssh_port)==True:
        print(f"SSH server {ssh_server_ip} is reachable.")
        logging.info(f"SSH server {ssh_server_ip} is reachable.")
        return True
    else:
        print("SSH Server is not port responding")
        return False
