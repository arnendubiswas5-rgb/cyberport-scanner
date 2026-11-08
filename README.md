\# 🛡️ CyberPort Scanner



\[!\[Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)

\[!\[Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)

\[!\[License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

\[!\[Status](https://img.shields.io/badge/Status-Active-success.svg)]()



A professional, cloud-powered network reconnaissance web application built with Python and Streamlit. Designed for cybersecurity enthusiasts, students, and network administrators to quickly identify open ports and running services on target domains without local network restrictions.



 \*\*\[Live Demo](YOUR\_LIVE\_STREAMLIT\_LINK\_HERE)\*\* \*(Click here to try it out instantly!)\*



\---



\## 📑 Table of Contents

\- \[About the Project](#-about-the-project)

\- \[Key Features](#-key-features)

\- \[How It Works](#-how-it-works)

\- \[Tech Stack](#-tech-stack)

\- \[Getting Started](#-getting-started)

\- \[Deployment](#-deployment)

\- \[Legal \& Ethical Disclaimer](#-legal--ethical-disclaimer)

\- \[Future Roadmap](#-future-roadmap)

\- \[Author](#-author)



\---
# CyberPort Scanner

A dual-mode network reconnaissance web application designed for port scanning and service fingerprinting. The tool abstracts the complexity of raw socket programming and API integration behind a unified Streamlit interface, allowing users to perform network analysis from a browser without local CLI dependencies.

**Live Deployment:** [cyberport-scanner-l59tuvrgehpqetjupwzvtp.streamlit.app](https://cyberport-scanner-l59tuvrgehpqetjupwzvtp.streamlit.app/)

---

## Overview

Standard port scanners like Nmap require local installation and direct network access. When deploying scanning tools to cloud-hosted web applications, outbound raw TCP socket connections are frequently blocked by the hosting provider's egress firewalls to prevent abuse. 

CyberPort Scanner solves this by implementing a dual-mode architecture. It defaults to a cloud-based API proxy for unrestricted scanning, but falls back to a highly optimized, multithreaded local socket scanner when specific port ranges are requested by the user.

---

## Architecture

The application operates in two distinct modes based on user input parameters:

### 1. Cloud API Mode (Default)
When no custom port range is specified, the backend dispatches an HTTPS GET request to the HackerTarget Nmap API. This delegates the actual network probing to an external infrastructure, completely bypassing the egress restrictions of the Streamlit hosting environment. The raw text response is parsed server-side to extract open ports and service banners.

### 2. Local Socket Mode
When a user specifies a custom port range (e.g., `1-100` or `80,443`), the application switches to Python's native `socket` library. To prevent the UI from freezing during sequential scans, it utilizes `concurrent.futures.ThreadPoolExecutor` with 50 worker threads. This allows for concurrent TCP connect scans, reducing the time required to scan 100 ports from ~100 seconds to ~2 seconds.

---

## Key Capabilities

- **Dual-Mode Execution:** Seamlessly transitions between API-based proxy scanning and raw multithreaded socket scanning.
- **Service Fingerprinting:** Attempts to read initial banners from open TCP ports to identify running software versions.
- **Concurrent Processing:** Local scans utilize a thread pool to execute parallel connection attempts.
- **Terminal Emulation UI:** Custom CSS injection overrides default Streamlit styling to provide a monospace, dark-themed interface that mimics a standard Linux terminal.

---

## Usage

The interface requires two inputs:

1. **Target IP or Domain:** The destination host (e.g., `scanme.nmap.org`, `192.168.1.1`).
2. **Custom Port Range (Optional):** 
   - Leave blank to trigger Cloud API Mode (scans top 1000 ports).
   - Enter a range (e.g., `1-1024`) or comma-separated list (e.g., `22,80,443`) to trigger Local Socket Mode.

---

## Local Development

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup and Execution

```bash
git clone https://github.com/arnendubiswas5-rgb/cyberport-scanner.git
cd cyberport-scanner

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch the application
python -m streamlit run app.py
