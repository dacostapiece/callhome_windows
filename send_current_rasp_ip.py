from dotenv import load_dotenv
import os
import subprocess
from config import ssh_username, ssh_server, ssh_port, ssh_server_filename, ssh_server_filename_directory

def write_ip_to_file_via_ssh(user, ssh_server, ip_address, filename, port, directory):

    #Construct the full path for the file
    remote_path = f"{directory}/{filename}"
    
    # Construct the SSH command for the standard port
    command_standard_port = f"ssh {user}@{ssh_server} \"echo '{ip_address}' > {remote_path}\""
    # Construct the SSH command for the alternative port
    command_alternative_port = f"ssh -p {port} {user}@{ssh_server} \"echo '{ip_address}' > {remote_path}\""
    
    print("Command to send (standard port):")
    print(command_standard_port)

    try:
        # Try executing the SSH command using the standard port
        result = subprocess.run(command_standard_port, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Print the output of the command
        print(f"Command output (standard port): {result.stdout.decode()}")
        print(result)

    except subprocess.CalledProcessError as e:
        # If it fails, try using the alternative port
        print(f"Command failed with error (standard port): {e.stderr.decode()}")
        print("Retrying with alternative port...")
        print("Command to send (alternative port):")
        print(command_alternative_port)
        
        try:
            # Execute the SSH command using the alternative port
            result = subprocess.run(command_alternative_port, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Print the output of the command
            print(f"Command output (alternative port): {result.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            # Print the error if the command fails again
            print(f"Command failed with error (alternative port): {e.stderr.decode()}")


def ssh_command(ip_address):
    write_ip_to_file_via_ssh(ssh_username, ssh_server, ip_address, ssh_server_filename, ssh_port, ssh_server_filename_directory)