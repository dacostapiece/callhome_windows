import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import mailserver, mailusername, mailpassword, source_mailaddress, dest_mailaddress, mailsubject_success, smtpport, mailsubject_failed, smtpport, mailsubject_success_updated
import sys

LOG_FILE = "/tmp/sendmail.log"

def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")


def send_mail_my_ip_is(currentIpAddress,ifconfig_run, currentIpAddressETH, currentIpAddressWLAN):
  
    #subject = mailsubject_success + currentIpAddress
    body = "This is an automated email.\n\nMy current TUN IP address is: " + currentIpAddress +"\n\n"
    body += "My current ETH IP address is: " + currentIpAddressETH +"\n\n"
    body += "My current WLAN IP address is: " + currentIpAddressWLAN +"\n"

    body += "\nIFCONFIG RUN\n"
    body += "" + ifconfig_run

    msg = MIMEMultipart()
    msg['From'] = source_mailaddress
    msg['To'] = dest_mailaddress
    msg['Subject'] = mailsubject_success + "TUN: "+ currentIpAddress + " ETH " + currentIpAddressETH + " WLAN " + currentIpAddressWLAN

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(mailserver, smtpport)
        server.starttls()
        server.login(mailusername, mailpassword)
        text = msg.as_string()
        server.sendmail(source_mailaddress, dest_mailaddress, text)

        server.quit()
        print("Email sent successfully!")
        log_message("Email sent successfully!")
    except Exception as e:
        log_message(f"Error: {e}")
        print("Error:", e)
        sys.exit(2)  # Failure

def send_mail_my_ip_is_updated(currentIpAddress,ifconfig_run, currentIpAddressETH, currentIpAddressWLAN):
  
    #subject = mailsubject_success + currentIpAddress
    body = "This is an automated email.\n\nMy current TUN IP address is: " + currentIpAddress +"\n\n"
    body += "My current ETH IP address is: " + currentIpAddressETH +"\n\n"
    body += "My current WLAN IP address is: " + currentIpAddressWLAN +"\n"

    body += "\nIFCONFIG RUN\n"
    body += "" + ifconfig_run

    msg = MIMEMultipart()
    msg['From'] = source_mailaddress
    msg['To'] = dest_mailaddress
    msg['Subject'] = mailsubject_success_updated + "TUN: "+ currentIpAddress + " ETH " + currentIpAddressETH + " WLAN " + currentIpAddressWLAN

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(mailserver, smtpport)
        server.starttls()
        server.login(mailusername, mailpassword)
        text = msg.as_string()
        server.sendmail(source_mailaddress, dest_mailaddress, text)

        server.quit()
        print("Update mail sent successfully!")
        log_message("Email sent successfully!")
    except Exception as e:
        log_message(f"Error: {e}")
        print("Error:", e)
        sys.exit(2)  # Failure

def send_mail_vpn_failed():
    body = "This is an automated email.\n\nThe VPN connection has failed."

    msg = MIMEMultipart()
    msg['From'] = source_mailaddress
    msg['To'] = dest_mailaddress
    msg['Subject'] = mailsubject_failed

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(mailserver, smtpport)
        server.starttls()
        server.login(mailusername, mailpassword)
        text = msg.as_string()
        server.sendmail(source_mailaddress, dest_mailaddress, text)
        server.quit()
        print("Email sent successfully!")
        log_message("Email sent successfully!")
    except Exception as e:
        print("Error:", e)
        log_message(f"Error: {e}")
        sys.exit(2)  # Failure

# Example usage:
# send_mail_my_ip_is("192.168.1.10")
# send_mail_vpn_failed()
