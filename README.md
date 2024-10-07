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
