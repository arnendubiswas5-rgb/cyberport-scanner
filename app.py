import streamlit as st
import requests

# ==========================================
# 1. PROFESSIONAL CUSTOM CSS
# ==========================================
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
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. UI LAYOUT
# ==========================================
st.markdown("<h1>🛡️ CYBERPORT SCANNER</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Cloud-powered reconnaissance tool | Scans top 1000 ports</p>", unsafe_allow_html=True)

target = st.text_input("Target IP or Domain", "scanme.nmap.org")

scan_button = st.button("🚀 INITIATE CLOUD SCAN", type="primary")

if scan_button:
    if not target:
        st.error("⚠️ Target is required.")
    else:
        status_text = st.empty()
        status_text.markdown(f"<div class='terminal-box'><span class='terminal-header'>root@cyberport:~#</span> Dispatching scan request for <b>{target}</b>...\nConnecting to cloud scanning engine...</div>", unsafe_allow_html=True)
        
        try:
            # Call the HackerTarget API (Runs the scan on their servers)
            url = f"https://api.hackertarget.com/nmap/?q={target}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                raw_data = response.text
                
                # Parse and format the API response into our terminal style
                terminal_output = f"root@cyberport:~# cloud-scan -t {target}\n"
                terminal_output += f"[*] Cloud engine initialized. Scanning top 1000 ports...\n"
                terminal_output += "-" * 45 + "\n"
                
                open_ports_count = 0
                for line in raw_data.splitlines():
                    # The API returns lines like "22/tcp  open  ssh"
                    if "open" in line and "STATE" not in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            port = parts[0]
                            service = parts[2]
                            terminal_output += f"[+] Port {port.ljust(8)} | Service: {service}\n"
                            open_ports_count += 1
                            
                terminal_output += "-" * 45 + "\n"
                if open_ports_count > 0:
                    terminal_output += f"[+] Scan Complete. Found {open_ports_count} open port(s).\n"
                else:
                    terminal_output += "[-] Scan Complete. No open ports found or target is blocking probes.\n"
                
                terminal_output += "root@cyberport:~# _"
                status_text.markdown(f'<div class="terminal-box">{terminal_output}</div>', unsafe_allow_html=True)
                
            else:
                status_text.markdown(f'<div class="terminal-box" style="color: #ff7b72;">[-] Error: Target unreachable or invalid IP/Domain provided.\nroot@cyberport:~# _</div>', unsafe_allow_html=True)
                
        except requests.exceptions.RequestException:
            status_text.markdown(f'<div class="terminal-box" style="color: #ff7b72;">[-] Error: Could not connect to scanning