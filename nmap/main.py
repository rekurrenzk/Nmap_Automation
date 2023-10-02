import subprocess
import time
import sys
import threading

def spinner(duration, control_event):
    spinner = '|/-\\'
    end_time = time.time() + duration
    while time.time() < end_time:
        if control_event.is_set():
            break
        for char in spinner:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

def get_current_ip():
    command = "hostname -I | awk '{print $1}'"
    my_ip = subprocess.getoutput(command)
    return my_ip

def log_system_status():
    command = "top -n 1 -b > system_status.log"
    subprocess.run(command, shell=True)

def send_notification():
    command = "notify-send 'Scan Complete' 'Your nmap scan has completed.'"
    subprocess.run(command, shell=True)


def scan_network(ip_range, control_event):
    try:
        vcompleted_process = subprocess.run(['nmap', '-sn', ip_range], capture_output=True, text=True, timeout=120)
        control_event.set()
        if completed_process.returncode == 0:
            output_lines = completed_process.stdout.split("\n")
            ip_addresses = [line.split()[1] for line in output_lines if "Nmap scan report for" in line]
            return ip_addresses
        else:
            print('Network scan failed')
            print('Error:')
            print(completed_process.stderr)
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def scan_ports(ip_address):
    try:
        completed_process = subprocess.run(['nmap', ip_address], capture_output=True, text=True)
        if completed_process.returncode == 0:
            print('Command succeeded')
            print('Output:')
            print(completed_process.stdout)
        else:
            print('Command failed')
            print('Error:')
            print(completed_process.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

# Control event for spinner thread
control_event = threading.Event()

# Start spinner as a separate thread
spinner_thread = threading.Thread(target=spinner, args=(60, control_event))  # The spinner will run for 60 seconds max
spinner_thread.start()

# Perform network scan to find active IP addresses
print("Scanning the network...")
ip_addresses = scan_network('192.168.0.0/24', control_event)  # Replace with your network's IP range

# Wait for spinner to finish, if it hasn't already
spinner_thread.join()

if ip_addresses:
    print("\nActive IP Addresses:")
    for index, ip in enumerate(ip_addresses):
        print(f"{index+1}. {ip}")

    # Allow user to choose an IP address to scan for ports
    user_choice = int(input("Select an IP address to scan for open ports (enter the corresponding number): ")) - 1
    if 0 <= user_choice < len(ip_addresses):
        selected_ip = ip_addresses[user_choice]
        print(f"Scanning ports for {selected_ip}...")
        scan_ports(selected_ip)
    else:
        print("Invalid choice. Exiting.")
else:
    print("No active IP addresses found.")

