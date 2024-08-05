import subprocess
import sys
import re

def run_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error executing command: {' '.join(command)}")
            print(f"Error output: {stderr}")
            return None
        return stdout
    except Exception as e:
        print(f"Error executing command: {e}")
        return None

def get_current_dns_mode(interface_name):
    output = run_command(["netsh", "interface", "ipv4", "show", "dns", interface_name])
    if output is None:
        return "unknown"
    
    if "DHCP" in output:
        return "auto"
    elif "Statically Configured DNS Servers" in output:
        return "man"
    else:
        return "unknown"

def get_current_dns_servers(interface_name):
    output = run_command(["netsh", "interface", "ipv4", "show", "dns", interface_name])
    if output is None:
        return []
    
    servers = re.findall(r"(\d+\.\d+\.\d+\.\d+)", output)
    return servers

def change_dns_settings(interface_name, mode, primary_dns=None, alternate_dns=None):

    current_mode = get_current_dns_mode(interface_name)
    print(f"Current DNS mode: {current_mode}")
    
    current_servers = get_current_dns_servers(interface_name)
    if current_servers:
        print(f"Current DNS servers: {', '.join(current_servers)}")
    else:
        print("Unable to retrieve current DNS servers.")

    try:
        print(mode.lower())
        if mode.lower() == "man":            
            # Set manual DNS
            run_command(["netsh", "interface", "ipv4", "set", "dns", 
                         f"name={interface_name}", "static", primary_dns])
            run_command(["netsh", "interface", "ipv4", "add", "dns", 
                         f"name={interface_name}", alternate_dns, "index=2"])
            
            # Enable DNS over HTTPS (DoH)
            run_command(["netsh", "dns", "add", "encryption", 
                         f"server={primary_dns}", "autoupgrade=yes"])
            run_command(["netsh", "dns", "add", "encryption", 
                         f"server={alternate_dns}", "autoupgrade=yes"])
            
            print(f"DNS settings changed to manual. Primary: {primary_dns}, Alternate: {alternate_dns}")
            print("DNS over HTTPS (DoH) enabled for both DNS servers.")
        
        elif mode.lower() == "auto":
            # Set automatic DNS (DHCP)
            run_command(["netsh", "interface", "ipv4", "set", "dns", 
                         f"name={interface_name}", "dhcp"])
            print("DNS settings changed to automatic (DHCP)")
        
        else:
            print("Invalid parameter. Use 'man' for manual, 'auto' for automatic DNS settings, or 'change' to specify custom DNS servers.")

    except Exception as e:
        print(f"Failed to change DNS settings: {str(e)}")
        print("Make sure you're running the script as administrator.")

def main():
    interface_name = "Wi-Fi"  # Change this to match your network interface name
    primary_dns_default = "8.8.8.8"  # Default primary DNS
    alternate_dns_default = "8.8.4.4"  # Default alternate DNS

    mode = "NULL"

    if len(sys.argv) < 2:
        print("Default: Flip mode from the Current...")
        mode = "flip"
    else:
        mode = sys.argv[1].lower()

    if mode == "help":
        print("Usage: python script_name.py [man|auto|check|change <primary_dns> <alternate_dns>]")
        print("More detail at: https://github.com/RiffuDev/DNS_Switcher")
        return

    elif mode == "check":
        current_mode = get_current_dns_mode(interface_name)
        print(f"Current DNS mode: {current_mode}")
        current_servers = get_current_dns_servers(interface_name)
        if current_servers:
            print(f"Current DNS servers: {', '.join(current_servers)}")
        else:
            print("Unable to retrieve current DNS servers.")

    elif mode == "flip":
        current_mode = get_current_dns_mode(interface_name)
        if(current_mode == "auto"):
            print(f"Fliping the mode to manual")
            change_dns_settings(interface_name,"man", primary_dns_default, alternate_dns_default)
        elif(current_mode == "man"):
            print(f"Fliping the mode to auto")
            change_dns_settings(interface_name,"auto", primary_dns_default, alternate_dns_default)
        else:
            print(f"Error: Current Dns Mode {current_mode}, Could'nt change!")

    elif mode == "change":
        if len(sys.argv) != 4:
            print("Usage for change: python script_name.py change primary_dns alternate_dns")
            print("Example: python script_name.py change 9.9.9.9 1.1.1.1")
        else:
            change_dns_settings(interface_name,"man", sys.argv[2], sys.argv[3])

    else:
        change_dns_settings(interface_name, sys.argv[1])

if __name__ == "__main__":
    main()