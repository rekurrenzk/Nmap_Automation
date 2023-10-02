# Bash command to get the IP address of the machine
my_ip=$(hostname -I | awk '{print $1}')

# Log CPU and Memory usage
top -n 1 -b > system_status.log

# Send desktop notification
notify-send 'Scan Complete' 'Your nmap scan has completed.'


