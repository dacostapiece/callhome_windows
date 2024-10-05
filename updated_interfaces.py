#!/usr/bin/env python3
import subprocess
import ipaddress
import sys
from sendmail import send_mail_my_ip_is_updated, send_mail_vpn_failed
import re
from writeandreadip_tunip import writeip
from myip_windows import is_ipv4, is_apipa_or_loopback
from config import home_dir

# Define the log file path for Windows
LOG_FILE = os.path.join(os.getcwd(), os.path.join(home_dir, "logs"), "updated_interfaces.log")
IFCONFIG_FILE = os.path.join(os.getcwd(), os.path.join(home_dir, "ipadd.txt"))

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(IFCONFIG_FILE), exist_ok=True)

#PHY INTERFACES TO LOOK FOR
interfaceETH_String = "Ethernet, Gigabit"
interfaceWLAN_String = 'Wireless 802.11'

#GET CURRENT NETWORK INFO with POWERSHELL
def get_interfaces_ipv4_from_ifconfig():
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
            if is_ipv4(ip_address):
                # Check if it's an APIPA (169.254.x.x) or loopback address (127.x.x.x)
                if not is_apipa_or_loopback(ip_address):  # Only add if it's not APIPA or loopback
                    tunnel_ipaddresses.append(ip_address)  # Append the valid tunnel IP address

        return tunnel_ipaddresses
            else:
            print("No IPv4 address found.")
            return None
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

#GET CURRENT IP FOR WLAN AND ETH0 WITH POWERSHELL
#TUN INTERFACES WORKS DIFFERENT - THERE'S AN UNIQUE FUNCTION TO GET TUN INFO
def get_network_interfaces(interface_pattern):
    """
    Retrieves network interfaces matching the given EthernetPattern.

    Parameters:
    EthernetPattern (str): A comma-separated string of patterns to match against adapter names.
    """
    # Convert EthernetPattern to a list, splitting by commas
    ethernet_patterns = [pattern.strip() for pattern in EthernetPattern.split(",")]
    
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
        
        ethernet_ipaddresses = []  # Store IP addresses for matching Ethernet adapters
        interface_count = 0
        
        # Iterate through interfaces and check for matching Ethernet adapters
        for interface in interfaces:
            ip_address = interface.get("IPAddress")
            adapter_name = interface.get("AdapterName")
            connection_name = interface.get("ConnectionName")
            
            # Increment interface count for display
            interface_count += 1

            # Check if the adapter matches any of the patterns in the EthernetPattern list
            if any(pattern in connection_name for pattern in ethernet_patterns):
 
                # Add the valid IP address to the list
                if is_ipv4(ip_address) and not is_apipa_or_loopback(ip_address):
                    ethernet_ipaddresses.append(ip_address)
        
        # Return the list of matching Ethernet IP addresses
        if ethernet_ipaddresses:
            print("Matching Ethernet IP Addresses:")
            for addr in ethernet_ipaddresses:
                print(f"  {addr}")
            return ethernet_ipaddresses
        else:
            print("No matching Ethernet adapters found.")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return False

#GET CURRENT TUN IP ADDRESS WITH POWERSHELL
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
                return addr
        else:
            print("No matching TAP-Windows Adapter with an IPv4 address found.")
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

def get_tun_ipv4():
    getValue = get_tun_interface_ipv4()
    if getValue != (None, None):
        return get_tun_interface_ipv4()
    else:
        return "None TUN iface", "None TUN ip"

def get_eth_ipv4():
    getValue = get_interface_ipv4(interfaceETH_String)
    if getValue !=  (None, None):
        return get_interface_ipv4(interfaceETH_String)
    else:
        return "None ETH iface", "None ETH ip"

def get_wlan_ipv4():
    getValue = get_interface_ipv4(interfaceWLAN_String)
    if getValue !=  (None, None):
        return get_interface_ipv4(interfaceWLAN_String)
    else:
        return "None WLAN iface", "None WLAN ip"

print("ifconfig run")    
a=get_tun_ipv4()
b=get_eth_ipv4()
#THIS ONE

c=get_wlan_ipv4()
print(a)
print(b)
print(c)

# Example usage:
interface, myIpAddress = get_tun_ipv4()
interfaceETH, myIpAddressETH = get_eth_ipv4()
interfaceWLAN, myIpAddressWLAN = get_wlan_ipv4()

#GET VARIABLES
# interface, myIpAddress = get_tun_ipv4_from_ifconfig()
# interfaceETH, myIpAddressETH = get_eth_ipv4_from_ifconfig()
# interfaceWLAN, myIpAddressWLAN = get_wlan_ipv4_from_ifconfig()
ifconfig_run = get_interfaces_ipv4_from_ifconfig()

#SUM ASCII CHAR FOR LATER COMPARISON
def sum_ascii_values(s):
    return sum(ord(char) for char in s)

#RETURN ASCII CHAR COMPARISON
def compare_ascii_sums(currentNetworkInfo, storedNetworkInfo):
    sum1 = sum(sum_ascii_values(value) for value in currentNetworkInfo)
    sum2 = sum(sum_ascii_values(value) for value in storedNetworkInfo)
    return sum1 == sum2
    
#OUTPUT LOG MESSAGE
def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")

#READ STORED IFCONFIG INFO
def read_ifconfig_stored():
    try:
        with open(IFCONFIG_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        Failed_Run_Message = " not found. myip.py didn't save run initial for some reason."
        log_message(f"{IFCONFIG_FILE}"+Failed_Run_Message)
        return f"{IFCONFIG_FILE}"+Failed_Run_Message

#SEND MAIL IF IPs HAVE CHANGED
def send_mail_if_needed():
    #NETWORK INFO WILL BE PULLED FROM HERE FOR MAIL SENDING
    send_mail_my_ip_is_updated(myIpAddress, ifconfig_run, myIpAddressETH, myIpAddressWLAN)
    writeip(myIpAddress)
    log_message("Interfaces have changed. Email notification sent.")

#READ STORED TUN INFO
def get_tun_ipv4_from_ifconfig_Stored(ifconfig_stored):
    try:
        #match = re.search(r'(tun\d+).*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ifconfig_stored, re.DOTALL)
        match = re.search(r'(tun\d+)(?:.*?\n){0,2}.*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ifconfig_stored)
        if match:
            interface, ipv4 = match.group(1), match.group(2)
            return interface, ipv4
        else:
            return None, None
    except Exception as e:
        log_message(f"Error parsing ifconfig output: {e}")
        return None, None

#READ STORED ETH0 INFO
def get_eth_ipv4_from_ifconfig_Stored(ifconfig_stored, interface_pattern):
    #interfaceETH_String = interfaceETH_String.decode("utf-8")
    try:
    #     #match = re.search(r'(eth\d+).*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ifconfig_stored, re.DOTALL)
    #     match = re.search(r'(eth\d+)(?:.*?\n){0,2}.*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ifconfig_stored)
    #     if match:
    #         interface, ipv4 = match.group(1), match.group(2)
    #         return interface, ipv4
    #     else:
    #         return None, None
    # except Exception as e:
    #     log_message(f"Error parsing ifconfig output: {e}")
    #     return None, None
        # Define regex pattern to find interfaces and IP addresses
        interface_pattern = rf'(\d+):\s({interface_pattern}):.*?state\s(\w+).*?inet\s(\d{{1,3}}\.\d{{1,3}}\.\d{{1,3}}\.\d{{1,3}})/\d+'
        matches = re.findall(interface_pattern, ifconfig_stored, re.DOTALL)
        
        # Debug: Print matches to verify
        #print(matches)
        
        # Loop through matches to find the first UP interface with an IP address
        for _, interface, state, ip_address in matches:
            if state == 'UP' and ip_address != "127.0.0.1":
                return interface, ip_address
        
        return None, None
    except subprocess.CalledProcessError:
        print("Error: Command 'ip addr show' failed.")
        return None, None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None, None
    
#READ STORED WLAN INFO
def get_wlan0_ipv4_from_ifconfig_Stored(ifconfig_stored, interface_pattern):
    #interfaceWLAN_String = interfaceWLAN_String.decode("utf-8")
    ifconfig_stored
    try:
    #     #match = re.search(r'(wlan\d+).*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ifconfig_stored, re.DOTALL)
    #     match = re.search(r'(wlan\d+)(?:.*?\n){0,2}.*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ifconfig_stored)
    #     if match:
    #         interface, ipv4 = match.group(1), match.group(2)
    #         return interface, ipv4
    #     else:
    #         return None, None
    # except Exception as e:
    #     log_message(f"Error parsing ifconfig output: {e}")
    #     return None, None
        interface_pattern = rf'(\d+):\s({interface_pattern}):.*?state\s(\w+).*?inet\s(\d{{1,3}}\.\d{{1,3}}\.\d{{1,3}}\.\d{{1,3}})/\d+'
        matches = re.findall(interface_pattern, ifconfig_stored, re.DOTALL)
        
        # Debug: Print matches to verify
        #print(matches)
        
        # Loop through matches to find the first UP interface with an IP address
        for _, interface, state, ip_address in matches:
            if state == 'UP' and ip_address != "127.0.0.1":
                return interface, ip_address
        
        return None, None
    except subprocess.CalledProcessError:
        print("Error: Command 'ip addr show' failed.")
        return None, None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None, None
   
#update ifconfig.txt to current interfaces info after comparison
def update_get_interfaces_ipv4_from_ifconfig():
    try:
        # Run the ifconfig command
        result = subprocess.check_output(["ip", "addr", "show"]).decode("utf-8")
        output = result

        if output!="":
                        # Save response to a file
            with open(IFCONFIG_FILE, "w") as file:
                file.write(output)
                print("Current ipadd stored to ipadd.txt")
            return output  # Return ifconfig run
        else:
            return None, None  # Return None ifconfig run
    except Exception as e:
        print("Error:", e)
        return None, None

#STARTS CHECKING NETWORK INFO FOR COMPARISON
if ifconfig_run is None:
    log_message("Failed to retrieve current ip addr show.")
    sys.exit(2)
else:
    ifconfig_stored = read_ifconfig_stored()

    def get_tun_ipv4_stored(ifconfig_stored):
        getValue = get_tun_ipv4_from_ifconfig_Stored(ifconfig_stored)
        if getValue != (None, None):
            return get_tun_ipv4_from_ifconfig_Stored(ifconfig_stored)
        else:
            return "None TUN iface", "None TUN ip"

    def get_eth_ipv4_stored(ifconfig_stored, interfaceETH_String):
        getValue = get_eth_ipv4_from_ifconfig_Stored(ifconfig_stored, interfaceETH_String)
        if getValue !=  (None, None):
            return get_eth_ipv4_from_ifconfig_Stored(ifconfig_stored, interfaceETH_String)
        else:
            return "None ETH iface", "None ETH ip"

    def get_wlan_ipv4_stored(ifconfig_stored, interfaceWLAN_String):
        getValue = get_wlan0_ipv4_from_ifconfig_Stored(ifconfig_stored, interfaceWLAN_String)
        if getValue !=  (None, None):
            return get_wlan0_ipv4_from_ifconfig_Stored(ifconfig_stored, interfaceWLAN_String)
        else:
            return "None WLAN iface", "None WLAN ip"

    d=get_tun_ipv4_stored(ifconfig_stored)
    e=get_eth_ipv4_stored(ifconfig_stored, interfaceETH_String)
    #THIS ONE

    f=get_wlan_ipv4_stored(ifconfig_stored, interfaceWLAN_String)

    # Call the function to get the interface name and IPv4 address associated with "tun" interface
    interfaceStored, myIpAddressStored = get_tun_ipv4_stored(ifconfig_stored)
    interfaceETHStored, myIpAddressETHStored = get_eth_ipv4_stored(ifconfig_stored, interfaceETH_String)
    interfaceWLANStored, myIpAddressWLANStored = get_wlan_ipv4_stored(ifconfig_stored, interfaceWLAN_String)

    # Call the function to get the interface name and IPv4 address associated with "tun" interface
    currentNetworkInfo = [interface, myIpAddress, interfaceETH, myIpAddressETH, interfaceWLAN, myIpAddressWLAN]
    storedNetworkInfo = [interfaceStored, myIpAddressStored, interfaceETHStored, myIpAddressETHStored, interfaceWLANStored, myIpAddressWLANStored]

    comparison_result = compare_ascii_sums(currentNetworkInfo, storedNetworkInfo)


    print("\n")
    print("ifconfig stored")    
    print(d)
    print(e)
    print(f)

    if comparison_result != True:
        send_mail_if_needed()
        update_get_interfaces_ipv4_from_ifconfig()
    else:
        print("Sem alterações de IP nas placas mais importantes.")
        None


# def ping_ip_address(stored_ip_address):
#     try:
#         # Run the ping command with 1 packet to check if the IP is reachable
#         result = subprocess.run(["ping", "-c", "1", stored_ip_address], capture_output=True, text=True)
        
#         # Check the return code to determine if the ping was successful
#         if result.returncode == 0:
#             return stored_ip_address
#         else:
#             return f"This {stored_ip_address} IP is not responding locally."
#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# # Example usage:
# stored_ip = myIpAddressETHStored
# result = ping_ip_address(stored_ip)
# print(result)
