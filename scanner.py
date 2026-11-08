import socket
import datetime

print("=== Advanced Port Scanner & Banner Grabber ===")
target = input("Enter target IP or domain (e.g., scanme.nmap.org): ").strip()

# Get port range from user
try:
    start_port = int(input("Enter starting port (e.g., 1): "))
    end_port = int(input("Enter ending port (e.g., 100): "))
except ValueError:
    print("Invalid input. Please enter numbers only.")
    exit()

print(f"\nStarting scan on {target} from port {start_port} to {end_port}...")
print("This may take a moment. Please wait.\n")

# Create a results file with a timestamp
filename = f"scan_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# Open the file in "write" mode ('w')
with open(filename, "w") as file:
    file.write(f"Scan Target: {target}\n")
    file.write(f"Port Range: {start_port} - {end_port}\n")
    file.write(f"Date: {datetime.datetime.now()}\n")
    file.write("-" * 50 + "\n")

    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1) # 1 second timeout for speed
            
            result = sock.connect_ex((target, port))
            
            if result == 0:
                print(f"[+] Port {port} is OPEN", end="")
                file.write(f"[+] Port {port} is OPEN")
                
                # Try to grab the banner
                try:
                    sock.send(b"\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    if banner:
                        print(f"  |  Service: {banner}")
                        file.write(f"  |  Service: {banner}\n")
                    else:
                        print()
                        file.write("\n")
                except:
                    print()
                    file.write("\n")
                    
            sock.close()
            
        except Exception:
            pass # Silently ignore errors to keep the scan running

print(f"\nScan complete! Results saved to: {filename}")