import subprocess
import json
import re

def get_network_interfaces():
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

            # Print interface details
            print(f"Interface {interface_count}:")
            print(f"  IP Address: {ip_address}")
            print(f"  Connection Name: {connection_name}")
            print(f"  Adapter Name: {adapter_name}")
            print()

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
                return addr
        else:
            print("No matching TAP-Windows Adapter with an IPv4 address found.")
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

def is_ipv4(ip_address):
    """Helper function to check if an IP address is IPv4 (not IPv6)."""
    return ip_address and ':' not in ip_address  # Simple check: IPv6 addresses contain ':'

def is_apipa_or_loopback(ip_address):
    """Helper function to check if an IP address is APIPA (169.254.x.x) or loopback (127.x.x.x)."""
    apipa_pattern = re.compile(r"^169\.254\.\d{1,3}\.\d{1,3}$")
    loopback_pattern = re.compile(r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    
    return bool(apipa_pattern.match(ip_address) or loopback_pattern.match(ip_address))

get_tun0_ip = get_network_interfaces()
