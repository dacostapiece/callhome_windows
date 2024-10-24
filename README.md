Callhome Windows

Download OpenVPN (not Connect version)

https://openvpn.net/community-downloads/
https://swupdate.openvpn.org/community/releases/OpenVPN-2.6.12-I001-amd64.msi

Install

Add it to path
C:\Program Files\OpenVPN\bin
System/Advanced Settings/Environment Variables
System variables - edit, add new

Close all prompt Windows
Test it
openvpn

Get *.ovpn file and create pass.txt like
username
password

Test it
openvpn --config "path\to\your\config.ovpn" --auth-user-pass pass.txt

add these lines below in *.ovpn file
auth-user-pass pass.txt
data-ciphers AES-256-CBC
tls-cipher "DEFAULT:@SECLEVEL=0"
then add *.ovpn file and pass.file to 
C:\Program Files\OpenVPN\config-auto
services.msc - logon as administrator username

schtasks /create /sc minute /mo 5 /tn "update_tun0_ipname" /tr "C:\Users\rafael\AppData\Local\Programs\Python\Python312\python.exe C:\callhome_windows\update_tun0_ipname.py" /ru SYSTEM /f

wevtutil set-log Microsoft-Windows-TaskScheduler/Operational /enabled:true


schtasks /create /sc minute /mo 5 /tn "update_tun0_ipname" /tr "python.exe C:\Users\rafael\Desktop\callhome_windows\update_tun0_ipname.py" /ru SYSTEM /f

Create Scheduled Task
schtasks /create /sc minute /mo 5 /tn "update_tun0_ipname" /tr "python.exe C:\path\to\file.py" /ru SYSTEM /f

install python
install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

install requests
pip install requests


install ping3
pip install ping3

install dotenv
pip install python-dotenv

Install Python
https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe

Add python.exe to PATH
Use admin privileges when installing
Install Now
Disable path length limit

Download Zip repository

Get .env sample and edit it
update config.py accordingly

get cloudflare api
get cloudflare zone id
get cloudflare dns id
update dns name

update home_dir

do not interrumpt battery
reactivate to run it

<h1>Sample .env</h1>

```bash
#.env

# Mail settings
mailserver = 'smtp.gmail.com'
smtpport = 587
mailusername = 'dacostapiecealerts@gmail.com'
mailpassword = 'bknd izkv zbhr jogq'
source_mailaddress = 'dacostapiecealerts@gmail.com'
dest_mailaddress = 'dacostapiecealerts@gmail.com'

# Remote VPN Target
vpn_probe_target = "10.0.10.1"

#API General Settings
api_token = "2a93dea3212543298c99b5216b0e5e12"
page_id = "qb7hs0ds4l0d"

#TESTE
env_var = "hello, i'm a env var"

# Cloudflare API credentials
CF_API_TOKEN = 'Qv5b8bePRqrJNti0qifoPzLJpyq4NxZD1-nO4xaq'

# Cloudflare Zone ID and DNS record information
ZONE_ID = '615bfd2ecd68639dab792dbc57a2bdca'
DNS_RECORD_NAME = 'cw.dacostapiece.com.br'
DNS_RECORD_ID = '2e2f8b41f8b4b717150259f968f5f361'

# SSH settings
SSH_USER = 'kali'
SSH_SERVER = 'home.dacostapiece.com.br'
#SSH_SERVER = '192.168.12.162'
SSH_OPTIONS = '-M 0 -f -N -R 2220:localhost:22 -R 5910:localhost:5900 '
SSH_KEY_PASSWORD='SSH@2024/*'
KEY_FILE = '/home/dacosta/.ssh/dacrasp'
SSH_PORT = 22

#SSH SERVER
SSH_SERVER_FILENAME = "current_rasp_ip.txt"
ssh_server_filename_directory = "/home/kali/CALLHOME_SSH_SERVER"
```
