import os
from config import ssh_server_filename

def writeip(variable):
    """Write the value of a variable to a specified file."""
    with open(ssh_server_filename, 'w') as file:
        file.write(variable)

def readip():
    """Read an IP address from a file if it exists."""
    if not os.path.isfile(ssh_server_filename):
        return False
    
    with open(ssh_server_filename, 'r') as file:
        ip_address = file.read().strip()
    
    return ip_address