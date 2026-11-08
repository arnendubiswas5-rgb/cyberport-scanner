import streamlit as st
import requests
import socket
import concurrent.futures

st.set_page_config(page_title="CyberPort Scanner", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    h1 {
        color: #00ff41;
        text-align: center;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 14px;
        margin-bottom: 30px;
    }

    .stTextInput > div > div > input {
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 10px;
    }

    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        transform: translateY(-2px);
    }

    .terminal-box {
        background-color: #010409;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 20px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 14px;
        color: #7ee787;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        white-space: pre-wrap;
        line-height: 1.5;
    }
    .terminal-header {
        color: #8b949e;
        border-bottom: 1px solid #30363d;
        padding-bottom: 10px;
        margin-bottom: 10px;
        font-size: 12px;
    }
    .warning-box {
        background-color: #2d1b00;
        border: 1px solid #ff7b72;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 20px;
        color: #ff7b72;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

def scan_port_local(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            try:
                sock.send(b"\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                sock.close()
                return {"port": port, "service": banner if banner else "Unknown"}
            except:
                sock.close()
                return {"port": port, "service": "Unknown"}
        sock.close()
        return None
    except Exception:
        return None

def scan_with_api(target):
    try:
        url = "https://api.hackertarget.com/nmap/?q=" + target
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            raw_data = response.text
            results = []
            
            for line in raw_data.splitlines():
                if "open" in line and "STATE" not in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        port_num = parts[0].split('/')[0]
                        service = parts[2]
                        results.append({"port": int(port_num), "service": service})
            return results
        return []
    except:
        return []

st.markdown("<h1>🛡️ CYBERPORT SCANNER</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Cloud-powered reconnaissance tool with custom port range support</p>", unsafe_allow_html=True)

st.markdown("""
<div class="warning-box">
⚠️ <b>Note:</b> Custom port ranges use local socket scanning (works best when running locally). 
Cloud deployment may have network restrictions. Leave blank for cloud-based top 1000 ports scan.
</div>
""", unsafe_allow_html=True)

target = st.text_input("Target IP or Domain", "scanme.nmap.org")
port_range_input = st.text_input("Custom Port Range (Optional)", placeholder="e.g., 1-100 or 80,443,8080 or leave blank for top 1000")

scan_button = st.button("🚀 INITIATE SCAN", type="primary")

if scan_button:
    if not target:
        st.error("Target is required.")
    else:
        status_text = st.empty()
        loading_msg = "<div class='terminal-box'><span class='terminal-header'>root@cyberport:~#</span> Initializing scan for <b>" + target + "</b>...\n"
        
        if port_range_input.strip():
            loading_msg += "[*] Mode: Local socket scanning (custom range)\n"
        else:
            loading_msg += "[*] Mode: Cloud API scanning (top 1000 ports)\n"
        
        loading_msg += "Please wait...</div>"
        status_text.markdown(loading_msg, unsafe_allow_html=True)
        
        results = []
        
        if port_range_input.strip():
            try:
                if ',' in port_range_input:
                    ports_to_scan = [int(p.strip()) for p in port_range_input.split(',')]
                elif '-' in port_range_input:
                    start, end = port_range_input.split('-')
                    ports_to_scan = range(int(start.strip()), int(end.strip()) + 1)
                else:
                    ports_to_scan = [int(port_range_input.strip())]
                
                terminal_output = "root@cyberport:~# local-scan -t " + target + " -p " + port_range_input + "\n"
                terminal_output += "[*] Scanning " + str(len(ports_to_scan)) + " port(s) using multithreaded socket...\n"
                terminal_output += "-" * 45 + "\n"
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                    future_to_port = {executor.submit(scan_port_local, target, port): port for port in ports_to_scan}
                    for future in concurrent.futures.as_completed(future_to_port):
                        result = future.result()
                        if result:
                            results.append(result)
                
                for res in sorted(results, key=lambda x: x['port']):
                    terminal_output += "[+] Port " + str(res['port']).ljust(6) + " | Service: " + res['service'] + "\n"
                
                terminal_output += "-" * 45 + "\n"
                if results:
                    terminal_output += "[+] Scan Complete. Found " + str(len(results)) + " open port(s).\n"
                else:
                    terminal_output += "[-] Scan Complete. No open ports found.\n"
                
                terminal_output += "root@cyberport:~# _"
                status_text.markdown('<div class="terminal-box">' + terminal_output + '</div>', unsafe_allow_html=True)
                
            except ValueError:
                error_msg = '<div class="terminal-box" style="color: #ff7b72;">[-] Error: Invalid port range format. Use "1-100" or "80,443,8080"\nroot@cyberport:~# _</div>'
                status_text.markdown(error_msg, unsafe_allow_html=True)
            except Exception as e:
                error_msg = '<div class="terminal-box" style="color: #ff7b72;">[-] Error: ' + str(e) + '\nroot@cyberport:~# _</div>'
                status_text.markdown(error_msg, unsafe_allow_html=True)
        
        else:
            try:
                results = scan_with_api(target)
                
                terminal_output = "root@cyberport:~# cloud-scan -t " + target + "\n"
                terminal_output += "[*] Cloud engine initialized. Scanning top 1000 ports...\n"
                terminal_output += "-" * 45 + "\n"
                
                for res in sorted(results, key=lambda x: x['port']):
                    terminal_output += "[+] Port " + str(res['port']).ljust(6) + " | Service: " + res['service'] + "\n"
                
                terminal_output += "-" * 45 + "\n"
                if results:
                    terminal_output += "[+] Scan Complete. Found " + str(len(results)) + " open port(s).\n"
                else:
                    terminal_output += "[-] Scan Complete. No open ports found or target is blocking probes.\n"
                
                terminal_output += "root@cyberport:~# _"
                status_text.markdown('<div class="terminal-box">' + terminal_output + '</div>', unsafe_allow_html=True)
                
            except Exception as e:
                error_msg = '<div class="terminal-box" style="color: #ff7b72;">[-] Error: Could not connect to scanning API.\nroot@cyberport:~# _</div>'
                status_text.markdown(error_msg, unsafe_allow_html=True)