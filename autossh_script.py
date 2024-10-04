#!/usr/bin/env python3
import subprocess
import os
import sys
import socket
import time
import re
import logging
import psutil
import pexpect
from send_current_rasp_ip import ssh_command
from writeandreadip_tunip import readip
import pdb

from config import ssh_username, ssh_server, ssh_options, ssh_handling, ssh_port, check_status_string, check_interval, key_file, key_password

# Configure logging
logging.basicConfig(filename='/tmp/autossh_script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define the status string to check (adjust for different languages/environment)
check_status_string # Change as needed for different languages/environment

def is_ssh_server_available(host, port):
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

# Function to start ssh-agent and add SSH key
def start_ssh_agent_and_add_key():
    # Start ssh-agent
    ssh_agent_proc = subprocess.run(['ssh-agent', '-s'], capture_output=True, text=True, check=True)
    ssh_agent_output = ssh_agent_proc.stdout.strip()

    # Debug output
    print(f"ssh-agent output:\n{ssh_agent_output}")

    # Parse SSH_AUTH_SOCK and SSH_AGENT_PID from the output
    sock_match = re.search(r'SSH_AUTH_SOCK=(?P<sock>\S+);', ssh_agent_output)
    pid_match = re.search(r'SSH_AGENT_PID=(?P<pid>\d+);', ssh_agent_output)

    if not sock_match or not pid_match:
        logging.error("Failed to parse ssh-agent output.")
        print("Failed to parse ssh-agent output.")
    else:
        # Set the environment variables
        os.environ['SSH_AUTH_SOCK'] = sock_match.group('sock')
        os.environ['SSH_AGENT_PID'] = pid_match.group('pid')

    # Verify the environment variables are set
    print("SSH agent started with the following environment variables:")
    print(f"SSH_AUTH_SOCK: {os.environ.get('SSH_AUTH_SOCK')}")
    print(f"SSH_AGENT_PID: {os.environ.get('SSH_AGENT_PID')}")

    # Add SSH key to ssh-agent with passphrase using pexpect
    try:
        ssh_add_command = f'ssh-add {key_file}'
        logging.info(f"Running command: {ssh_add_command}")
        
        child = pexpect.spawn(ssh_add_command)
        child.expect('Enter passphrase for')
        child.sendline(key_password)
        child.expect(pexpect.EOF)
        
        # Print the output
        ssh_add_output = child.before.decode()
        print(ssh_add_output)


        
        if 'Identity added' not in ssh_add_output:
            logging.error(f"Failed to add SSH key: {ssh_add_output}")
            print(f"Failed to add SSH key: {ssh_add_output}")
            return False
        else:
            print("Success: SSH key added to agent.")
            return True
    except Exception as e:
        logging.error(f"Error while running ssh-add: {e}")
        print(f"Error while running ssh-add: {e}")
        return False

#NOTHING IS CALLING IT    
def restart_autossh():
    """ Restart autossh process. """
    try:
        subprocess.run(["killall", "autossh"], check=True)
        # subprocess.run(["pkill", "autossh"], check=True)
        logging.info("Stopped existing autossh process.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to stop autossh: {e}")

    try:
        start_autossh_process()
        # command = f'autossh {ssh_options} {ssh_username}@{ssh_username}'
        # subprocess.Popen(command, shell=True)
        logging.info("Restarting autossh process.")
    except Exception as e:
        logging.error(f"Failed to start autossh: {e}")

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
        print(f"Error resolving DNS for {hostname}: {e}")
        logging.error(f"Error resolving DNS for {hostname}: {e}")
        sys.exit(2)

def start_autossh(command, log_file):
    """ Start autossh process and redirect output to log file. """
    try:
        with open(log_file, 'a') as log:
            # Start autossh process in the background, redirecting both stdout and stderr to log file
            # subprocess.Popen(command, shell=True, stdout=log, stderr=subprocess.STDOUT)
            subprocess.Popen(command, shell=True, stdout=log, stderr=subprocess.STDOUT, preexec_fn=os.setpgrp)
            print("command\n", command)
            print("start_autossh worked it")
            #send current ip for remote vpn checking
            ipaddress = readip()
            ssh_command(ipaddress)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred starting autossh: {e}")
        logging.error(f"An error occurred starting autossh: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"Error starting autossh: {str(e)}")
        logging.error(f"Error starting autossh: {str(e)}")
        sys.exit(2)

def check_ssh_tunnel(ip_address, port, log_file):
    """ Check if SSH tunnel to IP address and port is established using psutil. """
    try:
        # Get all TCP connections
        connections = psutil.net_connections(kind='tcp')
        #pdb.set_trace()

        # Check if there is an established connection to ip_address:port
        for conn in connections:
            if conn.status == psutil.CONN_ESTABLISHED and conn.raddr and conn.raddr.ip == ip_address and conn.raddr.port == port:
                logging.info(f"SSH tunnel to {ip_address}:{port} is established.")
                print(f"SSH tunnel to {ip_address}:{port} is established.")
                
                return True
        
        # If no matching connection found
        logging.warning(f"No established SSH tunnel found to {ip_address}:{port}.")
        print(f"No established SSH tunnel found to {ip_address}:{port}.")
        check_run = f"No established SSH tunnel found to {ip_address}:{port}."
        print("Log file for this action")
        print(log_file)
        return check_run

    except Exception as e:
        logging.error(f"Error occurred during SSH tunnel check: {str(e)}")
        print(f"Error occurred during SSH tunnel check: {str(e)}")
        return False
    
#CHECK AUTOSSH RUNNING PROCESS
def check_autossh_process():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'autossh' in proc.info['name']:
            print(f"autossh process found with PID {proc.info['pid']}")
            return True
        return False

#Using logging.basicConfig
# def log_error(message):
#     """ Log error message to log file. """
#     log_file = '/tmp/autossh_script.log'
#     with open(log_file, 'a') as log:
#         log.write(f"Error: {message}\n")

# Main script logic
def start_autossh_process():
    # Resolve DNS to get SSH server IP address
    ssh_server_ip = resolve_dns(ssh_server)

    # Open the log file for writing (append mode to keep all output)
    log_file = '/tmp/autossh_script.log'

     # Check if the SSH server is reachable before starting autossh
    if is_ssh_server_available(ssh_server_ip, ssh_port)==True:
        print(f"SSH server {ssh_server_ip} is reachable.")
        logging.info(f"SSH server {ssh_server_ip} is reachable.")


        # Start ssh-agent and add SSH key
        if start_ssh_agent_and_add_key()==True:
             # Construct the autossh command
            autossh_command = f'autossh {ssh_options} {ssh_handling} {ssh_username}@{ssh_server}'

            # Proceed with autossh or other operations that require SSH key authentication
            # Start autossh process
            start_autossh(autossh_command, log_file)
            time.sleep(30)
            # Check SSH tunnel status
            check_run = check_ssh_tunnel(ssh_server_ip, ssh_port, log_file)

            # Check SSH tunnel Status
            #First might run successfuly, but for some reason, code doesn't get it, it needs to be called twice
            #Let sysctl call it twice
            print("Check SSH Tunnel Status\n")
            check_run_comparison=f"No established SSH tunnel found to {ssh_server_ip}:{ssh_port}."
            if check_run ==check_run_comparison:
                print("Check SSH Tunnel Failed.")
                logging.error("Check SSH Tunnel Failed.")
                sys.exit(1)
            else:
                print("Check SSH Tunnel Sucess.")
                logging.info("Check SSH Tunnel Sucess.")
                sys.exit(0)

        else:
            logging.error("Failed to start ssh-agent or add SSH key. Exiting.")
            print(("Failed to start ssh-agent or add SSH key. Exiting."))
            sys.exit(1)
    else:
        print(f"SSH server {ssh_server_ip} is not reachable.")
        logging.error(f"SSH server {ssh_server_ip} is not reachable.")
        logging.info("Running Restart AutoSSH")
        restart_autossh()
        sys.exit(1)

# # Write environment variables to a file
# with open("/home/dacosta/CALLHOME/LOCAL_TEST_VARIABLES/environ.txt", "w") as env_file:
#     for key, value in os.environ.items():
#         env_file.write(f"{key}={value}\n")


start_autossh_process()

check_autossh_process()

if not check_autossh_process():
    print("autossh process is not running!")