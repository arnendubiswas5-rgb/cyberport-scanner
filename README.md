\# 🛡️ CyberPort Scanner



\[!\[Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)

\[!\[Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)

\[!\[License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

\[!\[Status](https://img.shields.io/badge/Status-Active-success.svg)]()



A professional, cloud-powered network reconnaissance web application built with Python and Streamlit. Designed for cybersecurity enthusiasts, students, and network administrators to quickly identify open ports and running services on target domains without local network restrictions.



🔗 \*\*\[Live Demo](YOUR\_LIVE\_STREAMLIT\_LINK\_HERE)\*\* \*(Click here to try it out instantly!)\*



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



\## 📖 About the Project

Traditional port scanners (like Nmap) require local installation and are often blocked by home/office ISP firewalls or cloud hosting providers. \*\*CyberPort Scanner\*\* solves this by providing a sleek, web-based interface that delegates the heavy lifting to the HackerTarget Nmap API. This allows users to perform legitimate network reconnaissance from any device, anywhere, while maintaining a professional, terminal-style user experience.



\---



\## ✨ Key Features

\- \*\*☁️ Cloud-Powered Execution:\*\* Bypasses local firewall restrictions by utilizing the HackerTarget API for reliable, remote scanning.

\- \*\*⚡ Multithreaded Architecture:\*\* (In local mode) Capable of scanning multiple ports simultaneously for maximum efficiency.

\- \*\*💻 Authentic Terminal UI:\*\* Custom CSS styling provides a sleek, dark-mode, monospace interface that mimics a real Linux terminal.

\- \*\*🔍 Service Fingerprinting:\*\* Automatically parses raw scan data to extract and display open ports alongside their identified services (e.g., `22/tcp open ssh`).

\- \*\*📱 Fully Responsive:\*\* Optimized for seamless use on desktop, tablet, and mobile devices.



\---



\## ⚙️ How It Works

1\. The user inputs a target domain or IP address via the Streamlit web interface.

2\. The application constructs a secure HTTPS GET request to the HackerTarget API.

3\. The API performs the Nmap scan on its end and returns raw text data.

4\. The Python backend parses this data, filtering for "open" states and formatting it into a clean, readable terminal-style output.

5\. The results are instantly rendered on the frontend for the user.



\---



\## 🛠️ Tech Stack

\- \*\*Language:\*\* Python 3.12

\- \*\*Web Framework:\*\* Streamlit

\- \*\*Networking:\*\* `requests` library for API communication, `socket` (for local fallback)

\- \*\*Styling:\*\* Custom CSS (injected via `st.markdown`)

\- \*\*Version Control:\*\* Git \& GitHub



\---



\## 🚀 Getting Started



Want to run this tool locally on your own machine? Follow these steps:



\### Prerequisites

\- Python 3.8 or higher installed on your system.

\- Git installed for cloning the repository.



\### Installation

1\. \*\*Clone the repository:\*\*

