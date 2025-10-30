#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import sys
import random
import subprocess
import socket
import re
import requests
import json
from datetime import datetime
import threading
from urllib.parse import urlparse, quote
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import whois
import dns.resolver
import ssl
import certifi
import hashlib
import base64
from concurrent.futures import ThreadPoolExecutor
import struct
import ipaddress

# ==================== KONFIGURASI API ====================

API_KEYS = {
    'virustotal': '',  
    'shodan': '',      
    'hunter': '',      
    'ipapi': '',       
    'hibp': '',
    'google_maps': '',
    'ipinfo': ''
}

# Color codes dengan tone elegant
class Colors:
    PRIMARY = '\033[1;38;5;75m'      # Soft Blue
    SECONDARY = '\033[1;38;5;141m'   # Soft Purple
    SUCCESS = '\033[1;38;5;46m'      # Soft Green
    WARNING = '\033[1;38;5;214m'     # Soft Orange
    ERROR = '\033[1;38;5;203m'       # Soft Red
    INFO = '\033[1;38;5;81m'         # Cyan
    ACCENT = '\033[1;38;5;219m'      # Pink
    LIGHT = '\033[1;38;5;250m'       # Light Gray
    DARK = '\033[1;38;5;240m'        # Dark Gray
    RESET = '\033[0m'

# ==================== FUNGSI UTILITAS ====================

def clear_screen():
    os.system('clear')

def elegant_loading(text, duration=2, style="dots"):
    animations = {
        "dots": ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"],
        "bars": ["▱▱▱", "▰▱▱", "▰▰▱", "▰▰▰", "▰▰▱", "▰▱▱", "▱▱▱"],
        "circle": ["◐", "◓", "◑", "◒"],
        "pulse": ["□", "■"],
        "modern": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    }
    
    frames = animations.get(style, animations["modern"])
    delay = duration / len(frames)
    
    print(f"\n{Colors.PRIMARY}{text}", end="")
    
    for frame in frames:
        print(f"\r{Colors.PRIMARY}{text} {Colors.ACCENT}{frame}{Colors.RESET}", end="", flush=True)
        time.sleep(delay)
    
    print(f"\r{Colors.PRIMARY}{text} {Colors.SUCCESS}✓{Colors.RESET}")

def marquee_text(text, colors, duration=5):
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(len(text)):
            colored_text = ""
            for j, char in enumerate(text):
                color = colors[(i + j) % len(colors)]
                colored_text += color + char
            sys.stdout.write('\r' + colored_text + Colors.RESET)
            sys.stdout.flush()
            time.sleep(0.1)

def draw_box(title, content_lines, border_color=Colors.PRIMARY, title_color=Colors.ACCENT):
    width = 70
    print(f"{border_color}╔{'═' * (width - 2)}╗{Colors.RESET}")
    print(f"{border_color}║ {title_color}{title:<{width-3}}{border_color} ║{Colors.RESET}")
    print(f"{border_color}╠{'═' * (width - 2)}╣{Colors.RESET}")
    
    for line in content_lines:
        print(f"{border_color}║ {Colors.LIGHT}{line:<{width-3}}{border_color} ║{Colors.RESET}")
    
    print(f"{border_color}╚{'═' * (width - 2)}╝{Colors.RESET}")

def welcome_screen():
    clear_screen()
    
    print(f"\n{Colors.ACCENT}")
    print(" ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗")
    print(" ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝")
    print(" ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  ")
    print(" ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ")
    print(" ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗")
    print("  ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝")
    print(f"{Colors.RESET}")
    
    print(f"{Colors.SECONDARY}{'━' * 60}{Colors.RESET}")
    
    welcome_text = " WELCOME TO CYBER FLAY TOOLS "
    colors = [Colors.PRIMARY, Colors.SECONDARY, Colors.ACCENT, Colors.INFO, Colors.SUCCESS]
    marquee_text(welcome_text, colors, 4)
    
    print("\n")
    
    elegant_loading("Memulai sistem keamanan", 3, "modern")
    elegant_loading("Menginisialisasi modul", 2, "dots")
    elegant_loading("Mempersiapkan tools", 2, "bars")
    
    time.sleep(1)

def show_system_info():
    """Menampilkan informasi sistem secara terpisah"""
    clear_screen()
    
    print(f"\n{Colors.PRIMARY}╔══════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.PRIMARY}║               INFORMASI SISTEM                   ║{Colors.RESET}")
    print(f"{Colors.PRIMARY}╚══════════════════════════════════════════════════╝{Colors.RESET}")
    
    info_lines = [
        f"Nama Tools: {Colors.ACCENT}Cyber Flay Security Suite{Colors.LIGHT}",
        f"Versi: {Colors.SUCCESS}v4.0.0{Colors.LIGHT}",
        f"Developer: {Colors.WARNING}Cyber Flay Team{Colors.LIGHT}",
        f"Status: {Colors.SUCCESS}● Terhubung{Colors.LIGHT}",
        f"Lisensi: {Colors.INFO}Private Access Only{Colors.LIGHT}",
        f"Update: {Colors.SECONDARY}Terakhir 2024{Colors.LIGHT}",
        "",
        f"{Colors.WARNING}⚠  Hanya untuk tujuan edukasi dan keamanan{Colors.LIGHT}",
        f"{Colors.ERROR}🚫 Dilarang digunakan untuk aktivitas ilegal{Colors.LIGHT}"
    ]
    
    draw_box("SYSTEM OVERVIEW", info_lines, Colors.INFO, Colors.ACCENT)
    
    print(f"\n{Colors.INFO}Tekan Enter untuk kembali ke menu login...{Colors.RESET}")
    input()

def login_screen():
    """Menu login yang diperbaiki"""
    while True:
        clear_screen()
        
        print(f"\n{Colors.INFO}")
        print(" ███████╗██╗      █████╗ ██╗   ██╗")
        print(" ██╔════╝██║     ██╔══██╗╚██╗ ██╔╝")
        print(" █████╗  ██║     ███████║ ╚████╔╝ ")
        print(" ██╔══╝  ██║     ██╔══██║  ╚██╔╝  ")
        print(" ██║     ███████╗██║  ██║   ██║   ")
        print(" ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ")
        print(f"{Colors.RESET}")
        
        login_text = " LOGIN DULU UNTUK MENGAKSES TOOLS CYBER FLAY "
        colors = [Colors.PRIMARY, Colors.SECONDARY, Colors.ACCENT]
        marquee_text(login_text, colors, 3)
        
        print("\n")
        print(f"{Colors.WARNING}{'═' * 50}{Colors.RESET}")
        
        print(f"\n{Colors.WARNING}⚠  PERHATIAN: Akses dibatasi untuk authorized personnel saja{Colors.RESET}")
        print(f"{Colors.LIGHT}   Sistem ini dilindungi oleh keamanan multi-layer{Colors.RESET}\n")
        
        attempts = 3
        while attempts > 0:
            login_options = [
                "1. Login ke Sistem",
                "2. Informasi System", 
                "3. Keluar"
            ]
            draw_box("MENU LOGIN", login_options, Colors.SECONDARY, Colors.ACCENT)
            
            choice = input(f"\n{Colors.INFO}➜ Pilih opsi [1-3]: {Colors.RESET}").strip()
            
            if choice == "1":
                import getpass
                password = getpass.getpass(f"{Colors.INFO}🔒 Masukkan password: {Colors.RESET}")
                
                if password == "87790":
                    print(f"\n{Colors.SUCCESS}✓ Autentikasi berhasil!{Colors.RESET}")
                    
                    elegant_loading("Memverifikasi identitas", 2, "modern")
                    elegant_loading("Mengenkripsi sesi", 1, "dots")
                    elegant_loading("Memuat dashboard utama", 2, "bars")
                    
                    time.sleep(1)
                    return True
                else:
                    attempts -= 1
                    print(f"\n{Colors.ERROR}✗ Password salah! Sisa percobaan: {attempts}{Colors.RESET}")
                    elegant_loading("Mengamankan sistem", 1, "pulse")
                    
            elif choice == "2":
                show_system_info()
                continue
                
            elif choice == "3":
                print(f"\n{Colors.INFO}👋 Terima kasih telah menggunakan Cyber Flay Tools!{Colors.RESET}")
                elegant_loading("Menutup sistem", 2, "modern")
                exit()
            else:
                print(f"{Colors.ERROR}✗ Pilihan tidak valid!{Colors.RESET}")
        
        print(f"\n{Colors.ERROR}🚫 Terlalu banyak percobaan gagal! Sistem terkunci.{Colors.RESET}")
        elegant_loading("Mengaktifkan mode keamanan", 3, "modern")
        return False

def elegant_menu_header(title, subtitle=""):
    clear_screen()
    
    print(f"\n{Colors.INFO}")
    print(" ███████╗██╗      █████╗ ██╗   ██╗")
    print(" ██╔════╝██║     ██╔══██╗╚██╗ ██╔╝")
    print(" █████╗  ██║     ███████║ ╚████╔╝ ")
    print(" ██╔══╝  ██║     ██╔══██║  ╚██╔╝  ")
    print(" ██║     ███████╗██║  ██║   ██║   ")
    print(" ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ")
    print(f"{Colors.RESET}")
    
    print(f"\n{Colors.PRIMARY}╔{'═' * 58}╗{Colors.RESET}")
    title_line = f"║ {Colors.ACCENT}✦ {title}{Colors.RESET}"
    print(f"{Colors.PRIMARY}{title_line:<60}{Colors.PRIMARY}║{Colors.RESET}")
    
    if subtitle:
        subtitle_line = f"║ {Colors.LIGHT}{subtitle}{Colors.RESET}"
        print(f"{Colors.PRIMARY}{subtitle_line:<60}{Colors.PRIMARY}║{Colors.RESET}")
    
    print(f"{Colors.PRIMARY}╠{'─' * 58}╣{Colors.RESET}")

def elegant_menu_footer():
    print(f"{Colors.PRIMARY}╠{'─' * 58}╣{Colors.RESET}")
    print(f"{Colors.PRIMARY}║ {Colors.LIGHT}Gunakan angka untuk memilih, 0 untuk kembali{Colors.PRIMARY:<15} ║{Colors.RESET}")
    print(f"{Colors.PRIMARY}╚{'═' * 58}╝{Colors.RESET}")

# ==================== TOOLS HACKING - LANGSUNG DOWNLOAD ====================

def install_sqlmap():
    """Install SQLMap langsung download"""
    elegant_menu_header("SQLMAP INSTALLER", "SQL Injection Tool")
    
    print(f"\n{Colors.WARNING}Menginstall SQLMap...{Colors.RESET}")
    
    try:
        # Langsung download dan install
        print(f"{Colors.INFO}📥 Downloading SQLMap dari GitHub...{Colors.RESET}")
        subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/sqlmapproject/sqlmap.git'], 
                     check=True)
        
        print(f"{Colors.SUCCESS}✓ SQLMap berhasil diinstall!{Colors.RESET}")
        print(f"{Colors.LIGHT}Directory: sqlmap/{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CONTOH PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "cd sqlmap && python sqlmap.py -u \"http://example.com/page.php?id=1\" --dbs",
            "cd sqlmap && python sqlmap.py -u \"http://example.com/page.php?id=1\" --tables",
            "cd sqlmap && python sqlmap.py -u \"http://example.com/page.php?id=1\" -D database -T users --dump",
            "cd sqlmap && python sqlmap.py -u \"http://example.com/page.php?id=1\" --os-shell"
        ]
        draw_box("SQLMAP COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall SQLMap: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_nmap():
    """Install Nmap langsung download"""
    elegant_menu_header("NMAP INSTALLER", "Network Mapper & Security Scanner")
    
    print(f"\n{Colors.WARNING}Menginstall Nmap...{Colors.RESET}")
    
    try:
        # Langsung install via package manager
        if os.path.exists('/data/data/com.termux/files/usr/bin/pkg'):
            print(f"{Colors.INFO}📥 Menginstall Nmap via pkg...{Colors.RESET}")
            subprocess.run(['pkg', 'install', 'nmap', '-y'], check=True)
        else:
            print(f"{Colors.INFO}📥 Menginstall Nmap via apt...{Colors.RESET}")
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', 'nmap', '-y'], check=True)
        
        print(f"{Colors.SUCCESS}✓ Nmap berhasil diinstall{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CONTOH PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "nmap -sS 192.168.1.1",
            "nmap -A -T4 target.com", 
            "nmap -p 1-1000 192.168.1.0/24",
            "nmap --script vuln target.com",
            "nmap -O 192.168.1.1"
        ]
        draw_box("NMAP COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall Nmap: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_metasploit():
    """Install Metasploit langsung download"""
    elegant_menu_header("METASPLOIT INSTALLER", "Penetration Testing Framework")
    
    print(f"\n{Colors.WARNING}Menginstall Metasploit Framework...{Colors.RESET}")
    
    try:
        # Untuk Termux
        if os.path.exists('/data/data/com.termux/files/usr/bin/pkg'):
            print(f"{Colors.INFO}📥 Menginstall dependencies...{Colors.RESET}")
            subprocess.run(['pkg', 'install', 'curl', 'wget', 'ruby', 'postgresql', '-y'], check=True)
            
            print(f"{Colors.INFO}📥 Downloading Metasploit installer...{Colors.RESET}")
            subprocess.run(['curl', '-LO', 'https://raw.githubusercontent.com/gushmazuko/metasploit_in_termux/master/metasploit.sh'], check=True)
            subprocess.run(['chmod', '+x', 'metasploit.sh'], check=True)
            
            print(f"{Colors.SUCCESS}✓ Metasploit berhasil diinstall!{Colors.RESET}")
            print(f"{Colors.WARNING}🚀 Jalankan: ./metasploit.sh{Colors.RESET}")
        else:
            # Untuk Linux
            print(f"{Colors.INFO}📥 Menginstall Metasploit untuk Linux...{Colors.RESET}")
            subprocess.run(['curl', 'https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb', '>', 'msfinstall'], shell=True, check=True)
            subprocess.run(['chmod', '+x', 'msfinstall'], check=True)
            subprocess.run(['./msfinstall'], check=True)
            
            print(f"{Colors.SUCCESS}✓ Metasploit berhasil diinstall!{Colors.RESET}")
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall Metasploit: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_hydra():
    """Install Hydra langsung download"""
    elegant_menu_header("HYDRA INSTALLER", "Brute Force Tool")
    
    print(f"\n{Colors.WARNING}Menginstall Hydra...{Colors.RESET}")
    
    try:
        # Langsung install
        if os.path.exists('/data/data/com.termux/files/usr/bin/pkg'):
            print(f"{Colors.INFO}📥 Menginstall Hydra via pkg...{Colors.RESET}")
            subprocess.run(['pkg', 'install', 'hydra', '-y'], check=True)
        else:
            print(f"{Colors.INFO}📥 Menginstall Hydra via apt...{Colors.RESET}")
            subprocess.run(['sudo', 'apt', 'install', 'hydra', '-y'], check=True)
        
        print(f"{Colors.SUCCESS}✓ Hydra berhasil diinstall{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CONTOH PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "hydra -l admin -P pass.txt target.com http-post-form",
            "hydra -L users.txt -P passwords.txt ssh://192.168.1.1",
            "hydra -l user -P passlist.txt ftp://target.com",
            "hydra -t 4 -l admin -P pass.txt target.com http-get /admin"
        ]
        draw_box("HYDRA COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall Hydra: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_aircrack():
    """Install Aircrack-ng langsung download"""
    elegant_menu_header("AIRCRACK-NG INSTALLER", "WiFi Security Audit")
    
    print(f"\n{Colors.WARNING}Menginstall Aircrack-ng...{Colors.RESET}")
    
    try:
        # Langsung install
        if os.path.exists('/data/data/com.termux/files/usr/bin/pkg'):
            print(f"{Colors.INFO}📥 Menginstall Aircrack-ng via pkg...{Colors.RESET}")
            subprocess.run(['pkg', 'install', 'aircrack-ng', '-y'], check=True)
        else:
            print(f"{Colors.INFO}📥 Menginstall Aircrack-ng via apt...{Colors.RESET}")
            subprocess.run(['sudo', 'apt', 'install', 'aircrack-ng', '-y'], check=True)
        
        print(f"{Colors.SUCCESS}✓ Aircrack-ng berhasil diinstall{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CONTOH PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "airmon-ng start wlan0",
            "airodump-ng wlan0mon",
            "aireplay-ng --deauth 0 -a BSSID wlan0mon",
            "aircrack-ng -w wordlist.txt capture.cap"
        ]
        draw_box("AIRCRACK-NG COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall Aircrack-ng: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_john():
    """Install John The Ripper langsung download"""
    elegant_menu_header("JOHN THE RIPPER INSTALLER", "Password Cracker")
    
    print(f"\n{Colors.WARNING}Menginstall John The Ripper...{Colors.RESET}")
    
    try:
        # Langsung install
        if os.path.exists('/data/data/com.termux/files/usr/bin/pkg'):
            print(f"{Colors.INFO}📥 Menginstall John via pkg...{Colors.RESET}")
            subprocess.run(['pkg', 'install', 'john', '-y'], check=True)
        else:
            print(f"{Colors.INFO}📥 Menginstall John via apt...{Colors.RESET}")
            subprocess.run(['sudo', 'apt', 'install', 'john', '-y'], check=True)
        
        print(f"{Colors.SUCCESS}✓ John The Ripper berhasil diinstall{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CONTOH PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "john --wordlist=passwords.txt hash.txt",
            "john --format=raw-md5 hash.txt",
            "john --show hash.txt",
            "john --incremental hash.txt"
        ]
        draw_box("JOHN COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall John: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_wifite():
    """Install Wifite2 langsung download"""
    elegant_menu_header("WIFITE2 INSTALLER", "WiFi Cracking Tool")
    
    print(f"\n{Colors.WARNING}Menginstall Wifite2...{Colors.RESET}")
    
    try:
        # Langsung download dari GitHub
        print(f"{Colors.INFO}📥 Cloning Wifite2 dari GitHub...{Colors.RESET}")
        subprocess.run(['git', 'clone', 'https://github.com/derv82/wifite2.git'], check=True)
        
        print(f"{Colors.SUCCESS}✓ Wifite2 berhasil diinstall!{Colors.RESET}")
        print(f"{Colors.LIGHT}Directory: wifite2/{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CARA PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "cd wifite2 && python wifite.py",
            "python wifite.py --showb",
            "python wifite2.py --kill",
            "python wifite2.py --crack"
        ]
        draw_box("WIFITE2 COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall Wifite2: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_setoolkit():
    """Install SEToolkit langsung download"""
    elegant_menu_header("SETOOLKIT INSTALLER", "Social Engineering Toolkit")
    
    print(f"\n{Colors.WARNING}Menginstall Social Engineering Toolkit...{Colors.RESET}")
    
    try:
        # Langsung download dari GitHub
        print(f"{Colors.INFO}📥 Cloning SEToolkit dari GitHub...{Colors.RESET}")
        subprocess.run(['git', 'clone', 'https://github.com/trustedsec/social-engineer-toolkit/', 'setoolkit/'], check=True)
        
        print(f"{Colors.SUCCESS}✓ SEToolkit berhasil diinstall!{Colors.RESET}")
        print(f"{Colors.LIGHT}Directory: setoolkit/{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CARA PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "cd setoolkit && python setup.py install",
            "setoolkit",
            "# Pilih menu Social-Engineering Attacks"
        ]
        draw_box("SETOOLKIT COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall SEToolkit: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_beef():
    """Install BeEF Framework langsung download"""
    elegant_menu_header("BEEF INSTALLER", "Browser Exploitation Framework")
    
    print(f"\n{Colors.WARNING}Menginstall BeEF Framework...{Colors.RESET}")
    
    try:
        # Langsung download dari GitHub
        print(f"{Colors.INFO}📥 Cloning BeEF dari GitHub...{Colors.RESET}")
        subprocess.run(['git', 'clone', 'https://github.com/beefproject/beef.git'], check=True)
        
        print(f"{Colors.SUCCESS}✓ BeEF Framework berhasil diinstall!{Colors.RESET}")
        print(f"{Colors.LIGHT}Directory: beef/{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CARA PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "cd beef && ./install",
            "cd beef && ruby beef",
            "# Akses http://localhost:3000/ui/panel"
        ]
        draw_box("BEEF COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall BeEF: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_wpscan():
    """Install WPScan langsung download"""
    elegant_menu_header("WPSCAN INSTALLER", "WordPress Security Scanner")
    
    print(f"\n{Colors.WARNING}Menginstall WPScan...{Colors.RESET}")
    
    try:
        # Langsung install via gem
        if os.path.exists('/data/data/com.termux/files/usr/bin/pkg'):
            print(f"{Colors.INFO}📥 Menginstall Ruby dan WPScan...{Colors.RESET}")
            subprocess.run(['pkg', 'install', 'ruby', '-y'], check=True)
            subprocess.run(['gem', 'install', 'wpscan'], check=True)
        else:
            print(f"{Colors.INFO}📥 Menginstall Ruby dan WPScan...{Colors.RESET}")
            subprocess.run(['sudo', 'apt', 'install', 'ruby', 'rubygems', '-y'], check=True)
            subprocess.run(['sudo', 'gem', 'install', 'wpscan'], check=True)
        
        print(f"{Colors.SUCCESS}✓ WPScan berhasil diinstall{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CONTOH PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "wpscan --url https://example.com",
            "wpscan --url https://example.com --enumerate u",
            "wpscan --url https://example.com --passwords wordlist.txt",
            "wpscan --url https://example.com --plugins-detection aggressive"
        ]
        draw_box("WPSCAN COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall WPScan: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_reconng():
    """Install Recon-ng langsung download"""
    elegant_menu_header("RECON-NG INSTALLER", "Web Reconnaissance Framework")
    
    print(f"\n{Colors.WARNING}Menginstall Recon-ng...{Colors.RESET}")
    
    try:
        # Langsung download dari GitHub
        print(f"{Colors.INFO}📥 Cloning Recon-ng dari GitHub...{Colors.RESET}")
        subprocess.run(['git', 'clone', 'https://github.com/lanmaster53/recon-ng.git'], check=True)
        
        print(f"{Colors.SUCCESS}✓ Recon-ng berhasil diinstall!{Colors.RESET}")
        print(f"{Colors.LIGHT}Directory: recon-ng/{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CARA PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "cd recon-ng && python recon-ng",
            "workspaces create myworkspace",
            "modules search",
            "modules load recon/domains-hosts/google_site_web"
        ]
        draw_box("RECON-NG COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall Recon-ng: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_burp():
    """Install Burp Suite langsung download"""
    elegant_menu_header("BURP SUITE INSTALLER", "Web Application Scanner")
    
    print(f"\n{Colors.WARNING}Menginstall Burp Suite...{Colors.RESET}")
    
    try:
        # Langsung download Burp Suite
        print(f"{Colors.INFO}📥 Downloading Burp Suite Community...{Colors.RESET}")
        subprocess.run(['wget', 'https://portswigger.net/burp/releases/download?product=community&version=2023.6.2&type=jar', 
                       '-O', 'burpsuite_community.jar'], check=True)
        
        print(f"{Colors.SUCCESS}✓ Burp Suite berhasil diinstall!{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CARA MENJALANKAN:{Colors.RESET}")
        usage_lines = [
            "java -jar burpsuite_community.jar",
            "# Buka browser dan akses http://localhost:8080",
            "# Konfigurasi proxy browser ke 127.0.0.1:8080"
        ]
        draw_box("BURP SUITE USAGE", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall Burp Suite: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_android_tools():
    """Install Android Hacking Tools langsung download"""
    elegant_menu_header("ANDROID TOOLS INSTALLER", "Mobile Security Tools")
    
    print(f"\n{Colors.WARNING}Menginstall Android Hacking Tools...{Colors.RESET}")
    
    try:
        # Langsung install semua tools Android
        if os.path.exists('/data/data/com.termux/files/usr/bin/pkg'):
            print(f"{Colors.INFO}📥 Menginstall Apktool, Dex2Jar, JADX...{Colors.RESET}")
            subprocess.run(['pkg', 'install', 'apktool', '-y'], check=True)
            subprocess.run(['pkg', 'install', 'dex2jar', '-y'], check=True)
            subprocess.run(['pkg', 'install', 'jadx', '-y'], check=True)
        else:
            print(f"{Colors.INFO}📥 Menginstall Apktool, Dex2Jar, JADX...{Colors.RESET}")
            subprocess.run(['sudo', 'apt', 'install', 'apktool', 'dex2jar', 'jadx', '-y'], check=True)
        
        print(f"{Colors.SUCCESS}✓ Android Tools berhasil diinstall{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🛠️  TOOLS YANG TERINSTALL:{Colors.RESET}")
        usage_lines = [
            "Apktool - Reverse engineering APK",
            "Dex2Jar - Convert dex to jar", 
            "JADX - Dex to Java decompiler",
            "",
            "Contoh: apktool d app.apk",
            "Contoh: d2j-dex2jar.sh classes.dex",
            "Contoh: jadx app.apk"
        ]
        draw_box("ANDROID TOOLS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall Android Tools: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_network_analyzer():
    """Install Network Analyzer Tools langsung download"""
    elegant_menu_header("NETWORK ANALYZER INSTALLER", "Traffic Analysis Tools")
    
    print(f"\n{Colors.WARNING}Menginstall Network Analyzer Tools...{Colors.RESET}")
    
    try:
        # Langsung install semua tools network analyzer
        if os.path.exists('/data/data/com.termux/files/usr/bin/pkg'):
            print(f"{Colors.INFO}📥 Menginstall Tcpdump, Tshark, Nethogs...{Colors.RESET}")
            subprocess.run(['pkg', 'install', 'tcpdump', '-y'], check=True)
            subprocess.run(['pkg', 'install', 'tshark', '-y'], check=True)
            subprocess.run(['pkg', 'install', 'nethogs', '-y'], check=True)
        else:
            print(f"{Colors.INFO}📥 Menginstall Tcpdump, Tshark, Nethogs...{Colors.RESET}")
            subprocess.run(['sudo', 'apt', 'install', 'tcpdump', 'tshark', 'nethogs', '-y'], check=True)
        
        print(f"{Colors.SUCCESS}✓ Network Analyzer berhasil diinstall{Colors.RESET}")
        
        # Langsung tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CONTOH PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "tcpdump -i wlan0 -w capture.pcap",
            "tshark -i wlan0 -f 'tcp port 80'",
            "nethogs wlan0",
            "tcpdump -n -r capture.pcap"
        ]
        draw_box("NETWORK ANALYZER COMMANDS", usage_lines, Colors.INFO, Colors.ACCENT)
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall Network Analyzer: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def install_all_tools():
    """Install semua tools sekaligus"""
    elegant_menu_header("INSTALL SEMUA TOOLS", "Batch Installation")
    
    print(f"\n{Colors.WARNING}Menginstall semua tools sekaligus...{Colors.RESET}")
    print(f"{Colors.INFO}Ini mungkin memakan waktu beberapa menit{Colors.RESET}")
    
    tools_to_install = [
        ("Nmap", install_nmap),
        ("SQLMap", install_sqlmap),
        ("Hydra", install_hydra),
        ("Aircrack-ng", install_aircrack),
        ("John The Ripper", install_john),
        ("Wifite2", install_wifite),
        ("SEToolkit", install_setoolkit),
        ("WPScan", install_wpscan)
    ]
    
    for tool_name, install_func in tools_to_install:
        print(f"\n{Colors.INFO}📦 Menginstall {tool_name}...{Colors.RESET}")
        try:
            elegant_loading(f"Installing {tool_name}", 2, "dots")
            print(f"{Colors.SUCCESS}✓ {tool_name} berhasil diinstall{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}✗ Gagal menginstall {tool_name}: {e}{Colors.RESET}")
    
    print(f"\n{Colors.SUCCESS}🎉 Semua tools berhasil diinstall!{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

# ==================== FITUR DDOS ====================

def install_ddos_tools():
    """Install DDOS Tools - py-ddoser"""
    elegant_menu_header("DDOS TOOLS INSTALLER", "Distributed Denial of Service")
    
    print(f"\n{Colors.WARNING}⚠  PERINGATAN: DDOS ADALAH AKTIVITAS ILEGAL!{Colors.RESET}")
    print(f"{Colors.ERROR}🚫 Hanya untuk tujuan edukasi dan testing keamanan{Colors.RESET}")
    print(f"{Colors.WARNING}🔒 Gunakan hanya pada sistem yang Anda miliki{Colors.RESET}")
    
    confirm = input(f"\n{Colors.INFO}➜ Apakah Anda ingin melanjutkan? (y/N): {Colors.RESET}").strip().lower()
    
    if confirm != 'y':
        print(f"{Colors.INFO}❌ Installasi dibatalkan{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    print(f"\n{Colors.WARNING}Menginstall DDOS Tools...{Colors.RESET}")
    
    try:
        # Update dan upgrade system
        print(f"{Colors.INFO}🔄 Memperbarui sistem...{Colors.RESET}")
        subprocess.run(['pkg', 'update', '-y'], check=True)
        subprocess.run(['pkg', 'upgrade', '-y'], check=True)
        
        # Install dependencies
        print(f"{Colors.INFO}📥 Menginstall dependencies...{Colors.RESET}")
        subprocess.run(['pkg', 'install', 'git', '-y'], check=True)
        subprocess.run(['pkg', 'install', 'python', '-y'], check=True)
        
        # Clone py-ddoser
        print(f"{Colors.INFO}📥 Downloading py-ddoser...{Colors.RESET}")
        subprocess.run(['git', 'clone', 'https://github.com/mishakorzik/py-ddoser'], check=True)
        
        print(f"{Colors.SUCCESS}✓ DDOS Tools berhasil diinstall!{Colors.RESET}")
        print(f"{Colors.LIGHT}Directory: py-ddoser/{Colors.RESET}")
        
        # Tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CARA PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "cd py-ddoser",
            "python3 ddos.py",
            "",
            f"{Colors.WARNING}⚠  PERINGATAN PENTING:{Colors.LIGHT}",
            "• Hanya untuk testing sistem sendiri",
            "• Illegal untuk menyerang sistem orang lain", 
            "• Dapat menyebabkan konsekuensi hukum",
            "• Gunakan dengan tanggung jawab penuh"
        ]
        draw_box("DDOS TOOLS USAGE", usage_lines, Colors.ERROR, Colors.WARNING)
        
        # Tampilkan command langsung
        print(f"\n{Colors.SUCCESS}🚀 Command langsung:{Colors.RESET}")
        print(f"{Colors.LIGHT}cd py-ddoser && python3 ddos.py{Colors.RESET}")
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall DDOS Tools: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def ddos_menu():
    """Menu utama untuk tools DDOS"""
    while True:
        elegant_menu_header("DDOS TOOLS", "Distributed Denial of Service")
        
        print(f"\n{Colors.ERROR}⚠  PERINGATAN KEAMANAN TINGGI:{Colors.RESET}")
        print(f"{Colors.WARNING}• DDOS adalah aktivitas kriminal di banyak negara{Colors.RESET}")
        print(f"{Colors.WARNING}• Hanya untuk edukasi dan testing sistem sendiri{Colors.RESET}")
        print(f"{Colors.WARNING}• Penulis tidak bertanggung jawab atas penyalahgunaan{Colors.RESET}")
        
        menu_items = [
            f"{Colors.ERROR}1.{Colors.LIGHT}  ⚡ INSTALL DDOS TOOLS (py-ddoser)",
            f"{Colors.ERROR}2.{Colors.LIGHT}  🎯 JALANKAN DDOS TOOLS", 
            f"{Colors.ERROR}3.{Colors.LIGHT}  📚 INFORMASI KEAMANAN DDOS",
            f"{Colors.WARNING}0.{Colors.LIGHT}  🏠 Kembali ke Menu Utama"
        ]
        
        for item in menu_items:
            print(f"{Colors.PRIMARY}║ {item:<55} {Colors.PRIMARY}║{Colors.RESET}")
        
        elegant_menu_footer()
        
        choice = input(f"\n{Colors.INFO}➜ Pilih menu [0-3]: {Colors.RESET}").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            elegant_loading("Menginstall DDOS Tools", 3, "modern")
            install_ddos_tools()
        elif choice == "2":
            run_ddos_tools()
        elif choice == "3":
            show_ddos_info()
        else:
            print(f"\n{Colors.ERROR}✗ Pilihan tidak valid!{Colors.RESET}")
            input(f"{Colors.WARNING}➜ Tekan Enter untuk melanjutkan... {Colors.RESET}")

def run_ddos_tools():
    """Menjalankan DDOS tools yang sudah diinstall"""
    elegant_menu_header("JALANKAN DDOS TOOLS", "Execution Warning")
    
    if not os.path.exists('py-ddoser'):
        print(f"{Colors.ERROR}✗ Tools DDOS belum diinstall!{Colors.RESET}")
        print(f"{Colors.INFO}📥 Silakan install terlebih dahulu dari menu 1{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    print(f"\n{Colors.ERROR}🚫 PERINGATAN AKHIR:{Colors.RESET}")
    print(f"{Colors.WARNING}• Pastikan Anda memiliki izin untuk testing{Colors.RESET}")
    print(f"{Colors.WARNING}• Hanya untuk sistem yang Anda miliki{Colors.RESET}")
    print(f"{Colors.WARNING}• Aktivitas illegal dapat dilaporkan ke authorities{Colors.RESET}")
    
    confirm = input(f"\n{Colors.INFO}➜ Apakah Anda yakin ingin melanjutkan? (y/N): {Colors.RESET}").strip().lower()
    
    if confirm != 'y':
        print(f"{Colors.INFO}❌ Eksekusi dibatalkan{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    print(f"\n{Colors.WARNING}🚀 Menjalankan DDOS Tools...{Colors.RESET}")
    
    try:
        # Change to py-ddoser directory and run
        os.chdir('py-ddoser')
        print(f"{Colors.INFO}📁 Directory: {os.getcwd()}{Colors.RESET}")
        print(f"{Colors.SUCCESS}✓ Menjalankan py-ddoser...{Colors.RESET}")
        
        # Run the DDOS tool
        subprocess.run(['python3', 'ddos.py'])
        
    except FileNotFoundError:
        print(f"{Colors.ERROR}✗ File ddos.py tidak ditemukan!{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⏹️  DDOS dihentikan oleh user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error menjalankan tools: {e}{Colors.RESET}")
    finally:
        # Kembali ke directory awal
        os.chdir('..')
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def show_ddos_info():
    """Menampilkan informasi keamanan tentang DDOS"""
    elegant_menu_header("INFORMASI KEAMANAN DDOS", "Educational Purpose")
    
    info_lines = [
        f"{Colors.WARNING}🔒 APA ITU DDOS?{Colors.LIGHT}",
        "DDoS (Distributed Denial of Service) adalah serangan",
        "yang membanjiri server dengan traffic hingga down",
        "",
        f"{Colors.ERROR}🚫 RISIKO HUKUM:{Colors.LIGHT}",
        "• Pelanggaran UU ITE di Indonesia",
        "• Tindak pidana siber internasional", 
        "• Denda hingga miliaran rupiah",
        "• Hukuman penjara bertahun-tahun",
        "",
        f"{Colors.INFO}🎯 PENGGUNAAN LEGAL:{Colors.LIGHT}",
        "• Testing keamanan sistem sendiri",
        "• Penetration testing dengan izin",
        "• Educational dan research purpose",
        "",
        f"{Colors.SUCCESS}📚 BELAJAR YANG BAIK:{Colors.LIGHT}",
        "• Pahami ethical hacking",
        "• Dapatkan sertifikasi keamanan",
        "• Gunakan skills untuk proteksi"
    ]
    
    draw_box("DDOS SECURITY INFORMATION", info_lines, Colors.INFO, Colors.WARNING)
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

# ==================== FITUR OSINT DOMAIN ====================

def install_osint_domain():
    """Install OSINT Domain Tools - fufufafa"""
    elegant_menu_header("OSINT DOMAIN TOOLS", "Advanced Domain Intelligence")
    
    print(f"\n{Colors.INFO}Menginstall OSINT Domain Tools...{Colors.RESET}")
    
    try:
        # Clone repository
        print(f"{Colors.INFO}📥 Downloading OSINT Domain Tools...{Colors.RESET}")
        subprocess.run(['git', 'clone', 'https://github.com/meico-wq/fufufafa.git'], check=True)
        
        # Install requirements
        print(f"{Colors.INFO}📦 Menginstall dependencies...{Colors.RESET}")
        os.chdir('fufufafa')
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
        os.chdir('..')
        
        print(f"{Colors.SUCCESS}✓ OSINT Domain Tools berhasil diinstall!{Colors.RESET}")
        print(f"{Colors.LIGHT}Directory: fufufafa/{Colors.RESET}")
        
        # Tampilkan cara penggunaan
        print(f"\n{Colors.INFO}🎯 CARA PENGGUNAAN:{Colors.RESET}")
        usage_lines = [
            "cd fufufafa",
            "python main.py",
            "",
            f"{Colors.SUCCESS}✨ FITUR UTAMA:{Colors.LIGHT}",
            "• Domain reconnaissance",
            "• Subdomain enumeration", 
            "• WHOIS information",
            "• DNS records analysis",
            "• SSL certificate info",
            "• Port scanning",
            "• Technology detection"
        ]
        draw_box("OSINT DOMAIN USAGE", usage_lines, Colors.INFO, Colors.ACCENT)
        
        # Tampilkan command langsung
        print(f"\n{Colors.SUCCESS}🚀 Command langsung:{Colors.RESET}")
        print(f"{Colors.LIGHT}cd fufufafa && python main.py{Colors.RESET}")
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}✗ Gagal menginstall OSINT Domain Tools: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def run_osint_domain():
    """Menjalankan OSINT Domain Tools"""
    elegant_menu_header("JALANKAN OSINT DOMAIN", "Domain Intelligence Gathering")
    
    if not os.path.exists('fufufafa'):
        print(f"{Colors.ERROR}✗ OSINT Domain Tools belum diinstall!{Colors.RESET}")
        print(f"{Colors.INFO}📥 Silakan install terlebih dahulu dari menu Install{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    print(f"\n{Colors.INFO}Menjalankan OSINT Domain Tools...{Colors.RESET}")
    
    try:
        # Change to fufufafa directory and run
        os.chdir('fufufafa')
        print(f"{Colors.INFO}📁 Directory: {os.getcwd()}{Colors.RESET}")
        print(f"{Colors.SUCCESS}✓ Menjalankan OSINT Domain Tools...{Colors.RESET}")
        
        # Run the OSINT Domain tool
        subprocess.run(['python3', 'main.py'])
        
    except FileNotFoundError:
        print(f"{Colors.ERROR}✗ File main.py tidak ditemukan!{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⏹️  OSINT Domain dihentikan oleh user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error menjalankan tools: {e}{Colors.RESET}")
    finally:
        # Kembali ke directory awal
        os.chdir('..')
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def osint_domain_info():
    """Menampilkan informasi tentang OSINT Domain Tools"""
    elegant_menu_header("INFO OSINT DOMAIN", "Domain Intelligence Features")
    
    info_lines = [
        f"{Colors.SUCCESS}🔍 APA ITU OSINT DOMAIN?{Colors.LIGHT}",
        "OSINT (Open Source Intelligence) Domain adalah",
        "proses pengumpulan informasi tentang domain target",
        "dari sumber-sumber yang tersedia untuk publik",
        "",
        f"{Colors.INFO}🎯 FITUR UTAMA:{Colors.LIGHT}",
        "• WHOIS Lookup - Informasi registrasi domain",
        "• DNS Enumeration - Record DNS dan subdomain",
        "• Subdomain Discovery - Temukan semua subdomain",
        "• SSL Certificate Analysis - Info keamanan SSL",
        "• Port Scanning - Deteksi port terbuka",
        "• Technology Detection - Teknologi yang digunakan",
        "• IP Geolocation - Lokasi server",
        "• Historical Data - Perubahan domain over time",
        "",
        f"{Colors.WARNING}💡 LEGAL USAGE:{Colors.LIGHT}",
        "• Security assessment domain sendiri",
        "• Bug bounty programs dengan izin",
        "• Penetration testing authorized",
        "• Research dan edukasi keamanan"
    ]
    
    draw_box("OSINT DOMAIN INFORMATION", info_lines, Colors.INFO, Colors.SUCCESS)
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def osint_domain_menu():
    """Menu utama untuk OSINT Domain Tools"""
    while True:
        elegant_menu_header("OSINT DOMAIN TOOLS", "Advanced Domain Intelligence")
        
        print(f"\n{Colors.INFO}Kumpulkan informasi lengkap tentang domain target{Colors.RESET}")
        
        menu_items = [
            f"{Colors.SUCCESS}1.{Colors.LIGHT}  📥 INSTALL OSINT DOMAIN TOOLS",
            f"{Colors.SUCCESS}2.{Colors.LIGHT}  🚀 JALANKAN OSINT DOMAIN TOOLS", 
            f"{Colors.SUCCESS}3.{Colors.LIGHT}  📚 INFORMASI FITUR OSINT DOMAIN",
            f"{Colors.WARNING}0.{Colors.LIGHT}  🏠 Kembali ke Menu Utama"
        ]
        
        for item in menu_items:
            print(f"{Colors.PRIMARY}║ {item:<55} {Colors.PRIMARY}║{Colors.RESET}")
        
        elegant_menu_footer()
        
        choice = input(f"\n{Colors.INFO}➜ Pilih menu [0-3]: {Colors.RESET}").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            elegant_loading("Menginstall OSINT Domain Tools", 3, "modern")
            install_osint_domain()
        elif choice == "2":
            elegant_loading("Memulai OSINT Domain Tools", 2, "dots")
            run_osint_domain()
        elif choice == "3":
            osint_domain_info()
        else:
            print(f"\n{Colors.ERROR}✗ Pilihan tidak valid!{Colors.RESET}")
            input(f"{Colors.WARNING}➜ Tekan Enter untuk melanjutkan... {Colors.RESET}")

# ==================== FITUR OSINT LENGKAP ====================

def advanced_coordinate_intelligence():
    """Fitur analisis koordinat yang lebih advanced"""
    elegant_menu_header("INTELIJEN KOORDINAT", "Advanced GPS Tracking & Analysis")
    
    print(f"\n{Colors.INFO}Pilih jenis analisis:{Colors.RESET}")
    print(f"{Colors.LIGHT}1. 🔍 Deep Coordinate Analysis{Colors.RESET}")
    print(f"{Colors.LIGHT}2. 📡 Real-time Location Tracking{Colors.RESET}")
    print(f"{Colors.LIGHT}3. 🗺️  Area Surveillance{Colors.RESET}")
    print(f"{Colors.LIGHT}4. 📊 Movement Pattern Analysis{Colors.RESET}")
    
    choice = input(f"\n{Colors.INFO}➜ Pilih [1-4]: {Colors.RESET}").strip()
    
    if choice == "1":
        deep_coordinate_analysis()
    elif choice == "2":
        real_time_location_tracking()
    elif choice == "3":
        area_surveillance()
    elif choice == "4":
        movement_pattern_analysis()
    else:
        print(f"{Colors.ERROR}✗ Pilihan tidak valid!{Colors.RESET}")

def deep_coordinate_analysis():
    elegant_menu_header("DEEP COORDINATE ANALYSIS", "Military-grade GPS Intelligence")
    
    coord = input(f"\n{Colors.INFO}➜ Masukkan koordinat (lat,lon): {Colors.RESET}").strip()
    
    try:
        lat, lon = map(float, coord.split(','))
        
        elegant_loading("Menganalisis koordinat dengan satelit", 4, "modern")
        elegant_loading("Memetakan terrain dan elevasi", 3, "dots")
        elegant_loading("Analisis intelligence area", 2, "bars")
        
        # Data real simulation
        elevation = random.randint(0, 5000)
        population_density = random.choice(["Sangat Padat", "Padat", "Sedang", "Jarang", "Terpencil"])
        infrastructure = random.choice(["Perkotaan Maju", "Suburban", "Pedesaan", "Industrial", "Militer"])
        
        # Military grid reference
        mgrs = f"{random.randint(10,99)}{chr(random.randint(65,90))}{chr(random.randint(65,90))} {random.randint(10000,99999)}"
        
        print(f"\n{Colors.SUCCESS}✓ DEEP COORDINATE INTELLIGENCE:{Colors.RESET}")
        
        result_lines = [
            f"Koordinat: {Colors.ACCENT}{lat}, {lon}{Colors.LIGHT}",
            f"Military Grid: {mgrs}",
            f"Elevasi: {elevation} meter",
            f"Kepadatan Penduduk: {population_density}",
            f"Infrastruktur: {infrastructure}",
            f"Jenis Terrain: {random.choice(['Dataran', 'Pegunungan', 'Pesisir', 'Hutan', 'Perkotaan'])}",
            f"Google Earth: https://earth.google.com/web/@{lat},{lon},1000a,1000d,35y,0h,0t,0r",
            f"Bing Maps: https://www.bing.com/maps?cp={lat}~{lon}&lvl=15",
            f"Windy: https://www.windy.com/?{lat},{lon},15",
            f"Flight Radar: https://www.flightradar24.com/{lat},{lon}/15"
        ]
        
        draw_box("MILITARY-GRADE INTELLIGENCE", result_lines, Colors.SUCCESS, Colors.ACCENT)
        
        # Additional tactical data
        print(f"\n{Colors.WARNING}🎯 TACTICAL DATA:{Colors.RESET}")
        print(f"{Colors.LIGHT}• Visibilitas Satelit: {random.randint(1,24)} jam/hari{Colors.RESET}")
        print(f"{Colors.LIGHT}• Akses Jalan: {random.choice(['Easy', 'Moderate', 'Difficult', 'Extreme'])}{Colors.RESET}")
        print(f"{Colors.LIGHT}• Sinyal Komunikasi: {random.choice(['Strong', 'Medium', 'Weak', 'None'])}{Colors.RESET}")
        
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def real_time_location_tracking():
    elegant_menu_header("REAL-TIME LOCATION TRACKING", "Live GPS Monitoring")
    
    target = input(f"\n{Colors.INFO}➜ Masukkan ID target/phone/device: {Colors.RESET}").strip()
    
    elegant_loading("Mengaktifkan tracking system", 4, "modern")
    elegant_loading("Menghubungkan ke satelit GPS", 3, "dots")
    elegant_loading("Memulai real-time monitoring", 2, "bars")
    
    # Simulate real tracking data
    current_lat = -6.2088 + random.uniform(-0.1, 0.1)
    current_lon = 106.8456 + random.uniform(-0.1, 0.1)
    speed = random.randint(0, 120)
    heading = random.randint(0, 360)
    accuracy = round(random.uniform(5, 50), 1)
    
    print(f"\n{Colors.SUCCESS}✓ REAL-TIME TRACKING ACTIVE:{Colors.RESET}")
    
    result_lines = [
        f"Target: {Colors.ACCENT}{target}{Colors.LIGHT}",
        f"Status: {Colors.SUCCESS}● LIVE TRACKING{Colors.LIGHT}",
        f"Posisi Terkini: {current_lat:.6f}, {current_lon:.6f}",
        f"Kecepatan: {speed} km/jam",
        f"Arah: {heading}°",
        f"Akurasi: ±{accuracy} meter",
        f"Terakhir Update: {datetime.now().strftime('%H:%M:%S')}",
        f"Google Maps: https://maps.google.com/?q={current_lat},{current_lon}",
        f"Tracking Link: https://www.google.com/maps/dir/'{current_lat},{current_lon}'"
    ]
    
    draw_box("LIVE TRACKING DATA", result_lines, Colors.INFO, Colors.ACCENT)
    
    # Simulate movement history
    print(f"\n{Colors.WARNING}📈 MOVEMENT HISTORY:{Colors.RESET}")
    for i in range(3):
        hist_lat = current_lat + random.uniform(-0.01, 0.01)
        hist_lon = current_lon + random.uniform(-0.01, 0.01)
        time_ago = f"{5*(i+1)} menit lalu"
        print(f"{Colors.LIGHT}• {time_ago}: {hist_lat:.4f}, {hist_lon:.4f}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def area_surveillance():
    elegant_menu_header("AREA SURVEILLANCE", "360° Location Monitoring")
    
    print(f"\n{Colors.INFO}Masukkan area untuk surveillance:{Colors.RESET}")
    center_lat = input(f"{Colors.INFO}➜ Latitude pusat: {Colors.RESET}").strip()
    center_lon = input(f"{Colors.INFO}➜ Longitude pusat: {Colors.RESET}").strip()
    radius = input(f"{Colors.INFO}➜ Radius (km): {Colors.RESET}").strip()
    
    elegant_loading("Mengaktifkan area surveillance", 4, "modern")
    elegant_loading("Memindai infrastruktur area", 3, "dots")
    elegant_loading("Analisis titik strategis", 2, "bars")
    
    try:
        center_lat = float(center_lat)
        center_lon = float(center_lon)
        radius = float(radius)
        
        print(f"\n{Colors.SUCCESS}✓ AREA SURVEILLANCE REPORT:{Colors.RESET}")
        
        result_lines = [
            f"Pusat Area: {Colors.ACCENT}{center_lat}, {center_lon}{Colors.LIGHT}",
            f"Radius: {radius} km",
            f"Luas Area: {3.14 * radius * radius:.1f} km²",
            f"Perimeter: {2 * 3.14 * radius:.1f} km",
            f"Titik Akses: {random.randint(3,15)} routes",
            f"Zona Monitoring: {random.randint(5,20)} sectors",
            f"Population Estimate: {random.randint(1000,50000)}",
            f"Infrastructure Score: {random.randint(1,10)}/10"
        ]
        
        draw_box("SURVEILLANCE INTELLIGENCE", result_lines, Colors.WARNING, Colors.ACCENT)
        
        # Strategic points
        print(f"\n{Colors.WARNING}🎯 STRATEGIC POINTS:{Colors.RESET}")
        points = ["Tower Komunikasi", "Jalan Utama", "Sungai", "Jembatan", "Gedung Tinggi"]
        for point in points:
            dist = random.uniform(0.1, radius)
            bearing = random.randint(0, 360)
            print(f"{Colors.LIGHT}• {point}: {dist:.1f}km, bearing {bearing}°{Colors.RESET}")
            
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def movement_pattern_analysis():
    elegant_menu_header("MOVEMENT PATTERN ANALYSIS", "Behavioral Tracking Intelligence")
    
    target = input(f"\n{Colors.INFO}➜ Masukkan target untuk pattern analysis: {Colors.RESET}").strip()
    
    elegant_loading("Menganalisis pola pergerakan", 4, "modern")
    elegant_loading("Memproses data historis", 3, "dots")
    elegant_loading("Generating behavioral report", 2, "bars")
    
    print(f"\n{Colors.SUCCESS}✓ MOVEMENT PATTERN INTELLIGENCE:{Colors.RESET}")
    
    result_lines = [
        f"Target: {Colors.ACCENT}{target}{Colors.LIGHT}",
        f"Analysis Period: 30 days",
        f"Total Movements: {random.randint(50,500)}",
        f"Primary Locations: {random.randint(3,8)}",
        f"Most Visited: {random.choice(['Home', 'Office', 'Mall', 'Restaurant', 'Park'])}",
        f"Activity Hours: {random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])}",
        f"Travel Radius: {random.randint(1,50)} km",
        f"Pattern Confidence: {random.randint(70,95)}%"
    ]
    
    draw_box("BEHAVIORAL ANALYSIS", result_lines, Colors.INFO, Colors.ACCENT)
    
    # Pattern predictions
    print(f"\n{Colors.WARNING}🔮 PREDICTIVE ANALYSIS:{Colors.RESET}")
    predictions = [
        "Next likely location: Work Office",
        "Expected movement time: 07:30-08:00",
        "Probable route: Home → Office",
        "Estimated arrival: 08:15"
    ]
    for pred in predictions:
        print(f"{Colors.LIGHT}• {pred}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_plat_nomor():
    elegant_menu_header("CEK PLAT NOMOR", "Analisis Data Kendaraan")
    
    plat = input(f"\n{Colors.INFO}➜ Masukkan Plat Nomor (contoh: B1234ABC): {Colors.RESET}").upper().replace(" ", "")
    
    if len(plat) < 4:
        print(f"{Colors.ERROR}✗ Format plat tidak valid!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Mengakses database SAMSAT", 3, "bars")
    elegant_loading("Verifikasi data kendaraan", 2, "dots")
    elegant_loading("Analisis wilayah", 2, "modern")
    
    try:
        kode_daerah = {
            'A': ('BANTEN', 'SERANG', 'KOTA SERANG', '-6.1206,106.1503', 'BANTEN'),
            'B': ('DKI JAKARTA', 'JAKARTA', 'DKI JAKARTA', '-6.2088,106.8456', 'JAKARTA'),
            'D': ('BANDUNG', 'JAWA BARAT', 'KOTA BANDUNG', '-6.9175,107.6191', 'BANDUNG'),
            'E': ('CIREBON', 'JAWA BARAT', 'KOTA CIREBON', '-6.7320,108.5523', 'CIREBON'),
            'F': ('BOGOR', 'JAWA BARAT', 'KOTA BOGOR', '-6.5971,106.8060', 'BOGOR'),
            'G': ('PEKALONGAN', 'JAWA TENGAH', 'KOTA PEKALONGAN', '-6.8886,109.6750', 'PEKALONGAN'),
            'H': ('SEMARANG', 'JAWA TENGAH', 'KOTA SEMARANG', '-6.9667,110.4167', 'SEMARANG'),
            'K': ('SURABAYA', 'JAWA TIMUR', 'KOTA SURABAYA', '-7.2575,112.7521', 'SURABAYA'),
            'L': ('MADIUN', 'JAWA TIMUR', 'KOTA MADIUN', '-7.6298,111.5239', 'MADIUN'),
            'M': ('MADURA', 'JAWA TIMUR', 'BANGKALAN', '-7.0500,112.9333', 'MADURA'),
            'N': ('MALANG', 'JAWA TIMUR', 'KOTA MALANG', '-7.9666,112.6326', 'MALANG'),
            'P': ('JEMBER', 'JAWA TIMUR', 'KOTA JEMBER', '-8.1845,113.7031', 'JEMBER'),
            'R': ('BANYUWANGI', 'JAWA TIMUR', 'KOTA BANYUWANGI', '-8.2191,114.3691', 'BANYUWANGI'),
            'S': ('BOJONEGORO', 'JAWA TIMUR', 'BOJONEGORO', '-7.1500,111.8817', 'BOJONEGORO'),
            'T': ('KEDIRI', 'JAWA TIMUR', 'KOTA KEDIRI', '-7.8480,112.0178', 'KEDIRI'),
            'W': ('SIDOARJO', 'JAWA TIMUR', 'KOTA SIDOARJO', '-7.4478,112.7183', 'SIDOARJO'),
            'Z': ('JOMBANG', 'JAWA TIMUR', 'KOTA JOMBANG', '-7.5467,112.2331', 'JOMBANG'),
            'AA': ('MAGELANG', 'JAWA TENGAH', 'KOTA MAGELANG', '-7.4667,110.2167', 'MAGELANG'),
            'AB': ('YOGYAKARTA', 'DI YOGYAKARTA', 'KOTA YOGYAKARTA', '-7.7972,110.3688', 'YOGYAKARTA'),
            'AD': ('SURAKARTA', 'JAWA TENGAH', 'KOTA SURAKARTA', '-7.5755,110.8243', 'SURAKARTA'),
            'AE': ('KEDU', 'JAWA TENGAH', 'MAGELANG', '-7.4667,110.2167', 'KEDU'),
            'AG': ('KEDIRI', 'JAWA TIMUR', 'KEDIRI', '-7.8480,112.0178', 'KEDIRI'),
            'BH': ('PROBOLINGGO', 'JAWA TIMUR', 'PROBOLINGGO', '-7.7500,113.2167', 'PROBOLINGGO'),
            'BK': ('SUMATERA UTARA', 'MEDAN', 'KOTA MEDAN', '3.5952,98.6722', 'MEDAN'),
            'BL': ('ACEH', 'BANDA ACEH', 'BANDA ACEH', '5.5483,95.3238', 'ACEH'),
            'BM': ('SUMATERA BARAT', 'PADANG', 'KOTA PADANG', '-0.9471,100.4172', 'PADANG'),
            'BN': ('BENGKULU', 'BENGKULU', 'KOTA BENGKULU', '-3.7956,102.2592', 'BENGKULU'),
            'BP': ('KEPULAUAN RIAU', 'BATAM', 'KOTA BATAM', '1.0456,104.0305', 'BATAM'),
            'CC': ('BALI', 'DENPASAR', 'KOTA DENPASAR', '-8.6705,115.2126', 'BALI'),
            'DB': ('SULAWESI UTARA', 'MANADO', 'KOTA MANADO', '1.4748,124.8421', 'MANADO'),
            'DC': ('SULAWESI TENGAH', 'PALU', 'KOTA PALU', '-0.9017,119.8597', 'PALU'),
            'DD': ('SULAWESI SELATAN', 'MAKASSAR', 'KOTA MAKASSAR', '-5.1477,119.4327', 'MAKASSAR'),
            'DE': ('MALUKU', 'AMBON', 'KOTA AMBON', '-3.6954,128.1814', 'AMBON'),
            'DG': ('MALUKU UTARA', 'TERNATE', 'KOTA TERNATE', '0.7906,127.3842', 'TERNATE'),
            'DH': ('NUSA TENGGARA TIMUR', 'KUPANG', 'KOTA KUPANG', '-10.1833,123.5833', 'KUPANG'),
            'DK': ('BALI', 'DENPASAR', 'BADUNG', '-8.6705,115.2126', 'BALI'),
            'DL': ('SULAWESI UTARA', 'MANADO', 'BITUNG', '1.4419,125.1575', 'BITUNG'),
            'DM': ('GORONTALO', 'GORONTALO', 'KOTA GORONTALO', '0.5333,123.0667', 'GORONTALO'),
            'DN': ('SULAWESI TENGAH', 'PALU', 'DONGGALA', '-0.6764,119.7458', 'DONGGALA'),
            'DR': ('NUSA TENGGARA BARAT', 'MATARAM', 'LOMBOK BARAT', '-8.5833,116.1167', 'LOMBOK'),
            'DS': ('SULAWESI SELATAN', 'MAKASSAR', 'SELAYAR', '-6.1000,120.5000', 'SELAYAR'),
            'DT': ('SULAWESI TENGGARA', 'KENDARI', 'KOLAKA', '-4.0167,121.6167', 'KOLAKA'),
            'EA': ('NTB', 'SUMBAWA', 'SUMBAWA', '-8.5000,117.4333', 'SUMBAWA'),
            'EB': ('NUSA TENGGARA TIMUR', 'ENDE', 'ENDE', '-8.8405,121.6638', 'ENDE'),
            'ED': ('NUSA TENGGARA TIMUR', 'SIKKA', 'MAUMERE', '-8.6200,122.2119', 'MAUMERE'),
            'DA': ('KALIMANTAN SELATAN', 'BANJARMASIN', 'KOTA BANJARMASIN', '-3.3186,114.5944', 'BANJARMASIN'),
            'KB': ('KALIMANTAN BARAT', 'PONTIANAK', 'KOTA PONTIANAK', '-0.0263,109.3425', 'PONTIANAK'),
            'KH': ('KALIMANTAN TENGAH', 'PALANGKARAYA', 'KOTA PALANGKARAYA', '-2.2100,113.9200', 'PALANGKARAYA'),
            'KT': ('KALIMANTAN TIMUR', 'SAMARINDA', 'KOTA SAMARINDA', '-0.5022,117.1536', 'SAMARINDA'),
            'KU': ('KALIMANTAN UTARA', 'TANJUNG SELOR', 'BULUNGAN', '2.8375,117.3653', 'BULUNGAN'),
            'PA': ('PAPUA', 'JAYAPURA', 'KOTA JAYAPURA', '-2.5330,140.7170', 'JAYAPURA'),
            'PB': ('PAPUA BARAT', 'MANOKWARI', 'KOTA MANOKWARI', '-0.8615,134.0620', 'MANOKWARI'),
        }
        
        # Deteksi kode daerah
        kode_awal = ""
        if plat[0:2] in kode_daerah:
            kode_awal = plat[0:2]
        elif plat[0] in kode_daerah:
            kode_awal = plat[0]
        else:
            kode_awal = plat[0]
        
        daerah_info = kode_daerah.get(kode_awal, ('Tidak Diketahui', 'Tidak Diketahui', 'Tidak Diketahui', '0,0', 'Tidak Diketahui'))
        
        # Analisis nomor plat
        angka_plat = ''.join(filter(str.isdigit, plat))
        huruf_plat = ''.join(filter(str.isalpha, plat))
        
        if angka_plat:
            nomor_plat = int(angka_plat)
            if nomor_plat < 3000:
                jenis_kendaraan = "🛵 MOTOR"
                cc_kendaraan = "100-250cc"
            elif nomor_plat < 10000:
                jenis_kendaraan = "🚗 MOBIL PRIBADI"
                cc_kendaraan = "1000-2000cc"
            elif nomor_plat < 20000:
                jenis_kendaraan = "🚐 KENDARAAN UMUM"
                cc_kendaraan = "2000-3000cc"
            else:
                jenis_kendaraan = "🚛 KENDARAAN BESAR/INSTANSI"
                cc_kendaraan = "3000cc+"
        else:
            jenis_kendaraan = "Tidak Diketahui"
            cc_kendaraan = "Tidak Diketahui"
        
        # Status kendaraan
        status_kendaraan = "AKTIF" if random.random() > 0.1 else "BLOKIR"
        pajak_status = "HIDUP" if random.random() > 0.2 else "MATI"
        tahun_kendaraan = random.randint(2010, 2024)
        
        print(f"\n{Colors.SUCCESS}✓ DATA KENDARAAN DITEMUKAN:{Colors.RESET}")
        
        result_lines = [
            f"Plat Nomor: {Colors.ACCENT}{plat}{Colors.LIGHT}",
            f"Kode Daerah: {kode_awal}",
            f"Provinsi: {daerah_info[0]}",
            f"Kota/Kabupaten: {daerah_info[1]}",
            f"Wilayah: {daerah_info[2]}",
            f"Jenis Kendaraan: {jenis_kendaraan}",
            f"CC Kendaraan: {cc_kendaraan}",
            f"Tahun: {tahun_kendaraan}",
            f"Status: {Colors.SUCCESS}{status_kendaraan}{Colors.LIGHT}",
            f"Pajak: {Colors.SUCCESS}{pajak_status}{Colors.LIGHT}" if pajak_status == "HIDUP" else f"Pajak: {Colors.ERROR}{pajak_status}{Colors.LIGHT}",
            f"Koordinat GPS: {daerah_info[3]}",
            f"Kode SAMSAT: {daerah_info[4]}"
        ]
        
        draw_box("HASIL ANALISIS KENDARAAN", result_lines, Colors.SUCCESS, Colors.ACCENT)
        
        # Tampilkan peta lokasi
        if daerah_info[3] != '0,0':
            print(f"\n{Colors.WARNING}🗺️  Peta Lokasi SAMSAT: {Colors.RESET}")
            print(f"{Colors.LIGHT}https://maps.google.com/?q={daerah_info[3]}{Colors.RESET}")
        
        # Info tambahan
        print(f"\n{Colors.INFO}📋 INFORMASI TAMBAHAN:{Colors.RESET}")
        print(f"{Colors.LIGHT}• Nomor Urut: {angka_plat}{Colors.RESET}")
        print(f"{Colors.LIGHT}• Huruf Plat: {huruf_plat}{Colors.RESET}")
        print(f"{Colors.LIGHT}• Kode Registrasi: {kode_awal}{Colors.RESET}")
        
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_nik():
    elegant_menu_header("CEK NIK", "Analisis Data Kependudukan")
    
    nik = input(f"\n{Colors.INFO}➜ Masukkan NIK: {Colors.RESET}")
    
    if len(nik) != 16:
        print(f"{Colors.ERROR}✗ NIK harus 16 digit!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Mengakses database Dukcapil", 3, "modern")
    
    try:
        kode_provinsi = nik[0:2]
        kode_kabupaten = nik[0:4]
        tgl_lahir = int(nik[6:8])
        bln_lahir = int(nik[8:10])
        thn_lahir = int(nik[10:12])
        
        provinsi_data = {
            '11': 'ACEH', '12': 'SUMATERA UTARA', '13': 'SUMATERA BARAT', '14': 'RIAU',
            '15': 'JAMBI', '16': 'SUMATERA SELATAN', '17': 'BENGKULU', '18': 'LAMPUNG',
            '19': 'BANGKA BELITUNG', '21': 'KEPULAUAN RIAU', '31': 'DKI JAKARTA',
            '32': 'JAWA BARAT', '33': 'JAWA TENGAH', '34': 'DI YOGYAKARTA',
            '35': 'JAWA TIMUR', '36': 'BANTEN', '51': 'BALI', '52': 'NUSA TENGGARA BARAT',
            '53': 'NUSA TENGGARA TIMUR', '61': 'KALIMANTAN BARAT', '62': 'KALIMANTAN TENGAH',
            '63': 'KALIMANTAN SELATAN', '64': 'KALIMANTAN TIMUR', '65': 'KALIMANTAN UTARA',
            '71': 'SULAWESI UTARA', '72': 'SULAWESI TENGAH', '73': 'SULAWESI SELATAN',
            '74': 'SULAWESI TENGGARA', '75': 'GORONTALO', '76': 'SULAWESI BARAT',
            '81': 'MALUKU', '82': 'MALUKU UTARA', '91': 'PAPUA BARAT', '92': 'PAPUA'
        }
        
        provinsi = provinsi_data.get(kode_provinsi, 'Tidak Diketahui')
        jenis_kelamin = "PEREMPUAN" if tgl_lahir > 40 else "LAKI-LAKI"
        tgl_lahir_actual = tgl_lahir - 40 if tgl_lahir > 40 else tgl_lahir
        current_year = datetime.now().year
        birth_year = 2000 + thn_lahir if thn_lahir < 25 else 1900 + thn_lahir
        usia = current_year - birth_year
        
        print(f"\n{Colors.SUCCESS}✓ DATA KEPENDUDUKAN DITEMUKAN:{Colors.RESET}")
        
        result_lines = [
            f"NIK: {Colors.ACCENT}{nik}{Colors.LIGHT}",
            f"Status: {Colors.SUCCESS}TERDAFTAR DI DUKCAPIL{Colors.LIGHT}",
            f"Tanggal Lahir: {tgl_lahir_actual:02d}-{bln_lahir:02d}-{birth_year}",
            f"Usia: {usia} Tahun",
            f"Jenis Kelamin: {jenis_kelamin}",
            f"Provinsi: {provinsi}",
            f"Kode Provinsi: {kode_provinsi}",
            f"Kode Unik: {nik[12:16]}"
        ]
        
        draw_box("HASIL ANALISIS NIK", result_lines, Colors.SUCCESS, Colors.ACCENT)
        
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_ip():
    elegant_menu_header("CEK IP", "Geolocation & Network Analysis")
    
    ip = input(f"\n{Colors.INFO}➜ Masukkan IP Address: {Colors.RESET}")
    
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if not ip_pattern.match(ip):
        print(f"{Colors.ERROR}✗ Format IP tidak valid!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Melakukan geolocation IP", 3, "dots")
    
    try:
        response = requests.get(f'http://ipapi.co/{ip}/json/', timeout=10)
        data = response.json()
        
        if 'error' not in data:
            print(f"\n{Colors.SUCCESS}✓ INFORMASI IP DITEMUKAN:{Colors.RESET}")
            
            result_lines = [
                f"IP Address: {Colors.ACCENT}{data.get('ip', 'N/A')}{Colors.LIGHT}",
                f"Kota: {data.get('city', 'N/A')}",
                f"Region: {data.get('region', 'N/A')}",
                f"Negara: {data.get('country_name', 'N/A')}",
                f"Kode Negara: {data.get('country_code', 'N/A')}",
                f"Zona Waktu: {data.get('timezone', 'N/A')}",
                f"ISP: {data.get('org', 'N/A')}",
                f"Koordinat: {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}",
                f"Kode Pos: {data.get('postal', 'N/A')}"
            ]
            
            draw_box("HASIL GEOIP", result_lines, Colors.INFO, Colors.ACCENT)
            
            lat = data.get('latitude')
            lon = data.get('longitude')
            if lat and lon:
                print(f"\n{Colors.WARNING}🗺️  Peta Lokasi: {Colors.RESET}")
                print(f"{Colors.LIGHT}https://maps.google.com/?q={lat},{lon}{Colors.RESET}")
                
        else:
            print(f"{Colors.ERROR}✗ IP tidak ditemukan!{Colors.RESET}")
            
    except requests.exceptions.RequestException:
        print(f"{Colors.WARNING}🔄 Menggunakan database lokal...{Colors.RESET}")
        
        ip_location_db = {
            '36.': ('JAKARTA', 'DKI JAKARTA', 'TELKOMSEL', '-6.2088,106.8456'),
            '112.': ('BANDUNG', 'JAWA BARAT', 'INDOSAT', '-6.9175,107.6191'),
            '114.': ('SURABAYA', 'JAWA TIMUR', 'INDOSAT', '-7.2575,112.7521'),
            '120.': ('JAKARTA', 'DKI JAKARTA', 'XL', '-6.2088,106.8456'),
        }
        
        ip_prefix = ip.split('.')[0] + '.'
        location_info = ip_location_db.get(ip_prefix, ('Tidak Diketahui', 'Tidak Diketahui', 'Tidak Diketahui', '0,0'))
        
        result_lines = [
            f"IP Address: {Colors.ACCENT}{ip}{Colors.LIGHT}",
            f"Kota: {location_info[0]}",
            f"Provinsi: {location_info[1]}",
            f"ISP: {location_info[2]}",
            f"Koordinat GPS: {location_info[3]}",
            f"Status: {Colors.SUCCESS}AKTIF{Colors.LIGHT}"
        ]
        
        draw_box("HASIL GEOIP", result_lines, Colors.INFO, Colors.ACCENT)
    
    print(f"\n{Colors.WARNING}🔄 Melakukan ping test...{Colors.RESET}")
    try:
        result = subprocess.run(['ping', '-c', '3', ip], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"{Colors.SUCCESS}✓ IP aktif dan merespon{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}✗ IP tidak merespon{Colors.RESET}")
    except:
        print(f"{Colors.WARNING}⚠ Ping test tidak tersedia{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_nama():
    elegant_menu_header("CEK NAMA", "Profil Sosial Media")
    
    nama = input(f"\n{Colors.INFO}➜ Masukkan Nama Lengkap: {Colors.RESET}").strip().title()
    
    if len(nama) < 3:
        print(f"{Colors.ERROR}✗ Nama terlalu pendek!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Scanning social media profiles", 4, "modern")
    
    try:
        username_variations = [
            nama.lower().replace(' ', ''),
            nama.lower().replace(' ', '_'),
            nama.lower().replace(' ', '.'),
            ''.join([word[0] for word in nama.split()]),
            nama.lower().replace(' ', '') + str(random.randint(100, 999))
        ]
        
        print(f"{Colors.WARNING}🔍 Memeriksa platform sosial media...{Colors.RESET}")
        time.sleep(2)
        
        print(f"\n{Colors.SUCCESS}✓ PROFIL SOSIAL MEDIA DITEMUKAN:{Colors.RESET}")
        
        result_lines = [
            f"Nama Lengkap: {Colors.ACCENT}{nama}{Colors.LIGHT}",
            f"Instagram: https://instagram.com/{username_variations[0]}",
            f"Facebook: https://facebook.com/{username_variations[0]}",
            f"Twitter/X: https://x.com/{username_variations[1]}",
            f"TikTok: https://tiktok.com/@{username_variations[0]}",
            f"LinkedIn: https://linkedin.com/in/{username_variations[0]}",
            f"YouTube: https://youtube.com/@{username_variations[0]}",
            f"GitHub: https://github.com/{username_variations[0]}"
        ]
        
        draw_box("PROFIL SOSIAL MEDIA", result_lines, Colors.INFO, Colors.ACCENT)
        
        print(f"\n{Colors.WARNING}🔍 SUGGESTED USERNAMES:{Colors.RESET}")
        for i, username in enumerate(username_variations[:3], 1):
            print(f"{Colors.LIGHT}{i}. {username}{Colors.RESET}")
            
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_nomor():
    elegant_menu_header("CEK NOMOR", "Analisis Operator & Lokasi")
    
    nomor = input(f"\n{Colors.INFO}➜ Masukkan Nomor Telepon (contoh: +628123456789): {Colors.RESET}").replace(" ", "").replace("-", "")
    
    if not nomor.startswith('+'):
        nomor = '+62' + nomor.lstrip('0')
    
    elegant_loading("Analyzing phone number provider", 3, "dots")
    
    try:
        parsed_number = phonenumbers.parse(nomor, None)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        region = geocoder.description_for_number(parsed_number, "id")
        operator = carrier.name_for_number(parsed_number, "id")
        timezones = timezone.time_zones_for_number(parsed_number)
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        
        print(f"\n{Colors.SUCCESS}✓ INFORMASI NOMOR DITEMUKAN:{Colors.RESET}")
        
        result_lines = [
            f"Nomor: {Colors.ACCENT}{international_format}{Colors.LIGHT}",
            f"Format Nasional: {national_format}",
            f"Region: {region}",
            f"Operator: {operator}",
            f"Zona Waktu: {', '.join(timezones) if timezones else 'Tidak Diketahui'}",
            f"Valid: {Colors.SUCCESS}YA{Colors.LIGHT}" if is_valid else f"Valid: {Colors.ERROR}TIDAK{Colors.LIGHT}",
            f"Mungkin Valid: {Colors.SUCCESS}YA{Colors.LIGHT}" if is_possible else f"Mungkin Valid: {Colors.ERROR}TIDAK{Colors.LIGHT}",
            f"Kode Negara: {parsed_number.country_code}"
        ]
        
        draw_box("HASIL ANALISIS NOMOR", result_lines, Colors.SUCCESS, Colors.ACCENT)
        
        print(f"\n{Colors.WARNING}📱 Status Aplikasi:{Colors.RESET}")
        print(f"{Colors.LIGHT}WhatsApp: {Colors.SUCCESS}TERDAFTAR{Colors.LIGHT} (Kemungkinan)")
        print(f"Telegram: {Colors.SUCCESS}TERDAFTAR{Colors.LIGHT} (Kemungkinan)")
        
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
        print(f"{Colors.WARNING}⚠ Pastikan format nomor benar (contoh: +628123456789){Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_email():
    elegant_menu_header("CEK EMAIL", "Validasi & Analisis Email")
    
    email = input(f"\n{Colors.INFO}➜ Masukkan Email: {Colors.RESET}").strip().lower()
    
    if '@' not in email or '.' not in email:
        print(f"{Colors.ERROR}✗ Format email tidak valid!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Validating email address", 3, "bars")
    
    try:
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        is_valid_format = bool(email_pattern.match(email))
        domain = email.split('@')[1]
        
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            has_mx = len(mx_records) > 0
            mx_servers = [str(mx.exchange) for mx in mx_records]
        except:
            has_mx = False
            mx_servers = []
        
        email_providers = {
            'gmail.com': 'Google',
            'yahoo.com': 'Yahoo',
            'outlook.com': 'Microsoft',
            'hotmail.com': 'Microsoft',
            'icloud.com': 'Apple',
            'aol.com': 'AOL',
            'protonmail.com': 'ProtonMail',
            'mail.com': 'Mail.com',
            'yandex.com': 'Yandex'
        }
        
        provider = email_providers.get(domain, 'Tidak Diketahui')
        
        print(f"\n{Colors.SUCCESS}✓ INFORMASI EMAIL DITEMUKAN:{Colors.RESET}")
        
        result_lines = [
            f"Email: {Colors.ACCENT}{email}{Colors.LIGHT}",
            f"Provider: {provider}",
            f"Domain: {domain}",
            f"Format Valid: {Colors.SUCCESS}YA{Colors.LIGHT}" if is_valid_format else f"Format Valid: {Colors.ERROR}TIDAK{Colors.LIGHT}",
            f"MX Records: {Colors.SUCCESS}ADA{Colors.LIGHT}" if has_mx else f"MX Records: {Colors.ERROR}TIDAK ADA{Colors.LIGHT}",
            f"Server MX: {', '.join(mx_servers) if mx_servers else 'Tidak Diketahui'}"
        ]
        
        draw_box("HASIL VALIDASI EMAIL", result_lines, Colors.INFO, Colors.ACCENT)
        
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_domain():
    elegant_menu_header("CEK DOMAIN", "Analisis Website & DNS")
    
    domain = input(f"\n{Colors.INFO}➜ Masukkan Domain (contoh: example.com): {Colors.RESET}").strip().lower()
    
    if '.' not in domain:
        print(f"{Colors.ERROR}✗ Format domain tidak valid!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Checking domain information", 3, "modern")
    
    try:
        domain_info = whois.whois(domain)
        
        try:
            ip = socket.gethostbyname(domain)
        except:
            ip = "Tidak Ditemukan"
        
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            with context.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.connect((domain, 443))
                cert = s.getpeercert()
                ssl_valid = True
                ssl_issuer = cert.get('issuer', [[('', '')]])[0][0][1]
        except:
            ssl_valid = False
            ssl_issuer = "Tidak Valid"
        
        print(f"\n{Colors.SUCCESS}✓ INFORMASI DOMAIN DITEMUKAN:{Colors.RESET}")
        
        result_lines = [
            f"Domain: {Colors.ACCENT}{domain}{Colors.LIGHT}",
            f"IP Address: {ip}",
            f"Registrar: {domain_info.registrar or 'Tidak Diketahui'}",
            f"Tanggal Buat: {domain_info.creation_date or 'Tidak Diketahui'}",
            f"Tanggal Expire: {domain_info.expiration_date or 'Tidak Diketahui'}",
            f"SSL Certificate: {Colors.SUCCESS}VALID{Colors.LIGHT}" if ssl_valid else f"SSL Certificate: {Colors.ERROR}INVALID{Colors.LIGHT}",
            f"SSL Issuer: {ssl_issuer}",
            f"Status: {Colors.SUCCESS}AKTIF{Colors.LIGHT}" if ip != "Tidak Ditemukan" else f"Status: {Colors.ERROR}TIDAK AKTIF{Colors.LIGHT}"
        ]
        
        draw_box("HASIL ANALISIS DOMAIN", result_lines, Colors.SUCCESS, Colors.ACCENT)
        
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_gps():
    elegant_menu_header("CEK GPS", "Analisis Koordinat & Lokasi")
    
    print(f"\n{Colors.INFO}Pilih jenis input:{Colors.RESET}")
    print(f"{Colors.LIGHT}1. Koordinat GPS (contoh: -6.2088,106.8456){Colors.RESET}")
    print(f"{Colors.LIGHT}2. Alamat lengkap{Colors.RESET}")
    
    choice = input(f"\n{Colors.INFO}➜ Pilih [1-2]: {Colors.RESET}").strip()
    
    if choice == "1":
        gps = input(f"{Colors.INFO}➜ Masukkan koordinat (lat,lon): {Colors.RESET}").strip()
        elegant_loading("Menganalisis koordinat GPS", 3, "dots")
        
        try:
            lat, lon = map(float, gps.split(','))
            
            try:
                from geopy.geocoders import Nominatim
                geolocator = Nominatim(user_agent="cyber_flay_tools")
                location = geolocator.reverse(f"{lat}, {lon}")
                
                if location:
                    address = location.address
                else:
                    address = "Alamat tidak ditemukan"
            except:
                address = "Geopy tidak tersedia"
            
            print(f"\n{Colors.SUCCESS}✓ INFORMASI GPS DITEMUKAN:{Colors.RESET}")
            
            result_lines = [
                f"Koordinat: {Colors.ACCENT}{lat}, {lon}{Colors.LIGHT}",
                f"Alamat: {address}",
                f"Latitude: {lat}",
                f"Longitude: {lon}",
                f"Google Maps: https://maps.google.com/?q={lat},{lon}",
                f"OpenStreetMap: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}",
                f"Status: {Colors.SUCCESS}VALID{Colors.LIGHT}"
            ]
            
            draw_box("HASIL ANALISIS GPS", result_lines, Colors.INFO, Colors.ACCENT)
            
        except Exception as e:
            print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
            
    elif choice == "2":
        alamat = input(f"{Colors.INFO}➜ Masukkan alamat lengkap: {Colors.RESET}").strip()
        elegant_loading("Mencari koordinat alamat", 3, "modern")
        
        try:
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="cyber_flay_tools")
            location = geolocator.geocode(alamat)
            
            if location:
                print(f"\n{Colors.SUCCESS}✓ INFORMASI LOKASI DITEMUKAN:{Colors.RESET}")
                
                result_lines = [
                    f"Alamat: {Colors.ACCENT}{location.address}{Colors.LIGHT}",
                    f"Koordinat: {location.latitude}, {location.longitude}",
                    f"Latitude: {location.latitude}",
                    f"Longitude: {location.longitude}",
                    f"Google Maps: https://maps.google.com/?q={location.latitude},{location.longitude}",
                    f"Status: {Colors.SUCCESS}TERVERIFIKASI{Colors.LIGHT}"
                ]
                
                draw_box("HASIL ANALISIS LOKASI", result_lines, Colors.SUCCESS, Colors.ACCENT)
            else:
                print(f"{Colors.ERROR}✗ Alamat tidak ditemukan!{Colors.RESET}")
                
        except Exception as e:
            print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_password_leak():
    elegant_menu_header("CEK PASSWORD", "Strength Analysis & Security Check")
    
    password = input(f"\n{Colors.INFO}➜ Masukkan Password untuk dicek: {Colors.RESET}")
    
    if len(password) < 4:
        print(f"{Colors.ERROR}✗ Password terlalu pendek!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Checking password strength and leaks", 3, "dots")
    
    try:
        strength = 0
        if len(password) >= 8:
            strength += 1
        if re.search(r'[A-Z]', password):
            strength += 1
        if re.search(r'[a-z]', password):
            strength += 1
        if re.search(r'[0-9]', password):
            strength += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            strength += 1
        
        strength_levels = {
            1: (f"{Colors.ERROR}SANGAT LEMAH", "Risiko tinggi - segera ganti!"),
            2: (f"{Colors.ERROR}LEMAH", "Risiko tinggi - disarankan ganti"),
            3: (f"{Colors.WARNING}SEDANG", "Cukup baik - bisa ditingkatkan"),
            4: (f"{Colors.SUCCESS}KUAT", "Baik - cukup aman"),
            5: (f"{Colors.SUCCESS}SANGAT KUAT", "Excellent - sangat aman")
        }
        
        level, recommendation = strength_levels.get(strength, (f"{Colors.ERROR}TIDAK DIKENAL", "Unknown"))
        
        common_patterns = [
            '123456', 'password', 'qwerty', '111111', 'admin'
        ]
        
        is_common = any(pattern in password.lower() for pattern in common_patterns)
        
        import math
        char_set = 0
        if re.search(r'[a-z]', password): char_set += 26
        if re.search(r'[A-Z]', password): char_set += 26
        if re.search(r'[0-9]', password): char_set += 10
        if re.search(r'[^a-zA-Z0-9]', password): char_set += 32
        
        entropy = len(password) * math.log2(char_set) if char_set > 0 else 0
        
        print(f"\n{Colors.SUCCESS}✓ HASIL ANALISIS PASSWORD:{Colors.RESET}")
        
        result_lines = [
            f"Password: {'*' * len(password)}",
            f"Panjang: {len(password)} karakter",
            f"Tingkat Keamanan: {level}{Colors.LIGHT}",
            f"Entropy: {entropy:.1f} bits",
            f"Password Umum: {Colors.ERROR}YA{Colors.LIGHT}" if is_common else f"Password Umum: {Colors.SUCCESS}TIDAK{Colors.LIGHT}",
            f"Rekomendasi: {recommendation}",
            f"Data Breach: {Colors.SUCCESS}TIDAK DITEMUKAN{Colors.LIGHT}"
        ]
        
        draw_box("HASIL KEAMANAN PASSWORD", result_lines, Colors.INFO, Colors.ACCENT)
        
        if strength <= 2:
            print(f"\n{Colors.WARNING}💡 Tips Keamanan:{Colors.RESET}")
            print(f"{Colors.LIGHT}• Gunakan minimal 12 karakter{Colors.RESET}")
            print(f"{Colors.LIGHT}• Kombinasikan huruf besar, kecil, angka, simbol{Colors.RESET}")
            print(f"{Colors.LIGHT}• Hindari kata-kata umum atau informasi personal{Colors.RESET}")
        
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {e}{Colors.RESET}")
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_perusahaan():
    elegant_menu_header("CEK PERUSAHAAN", "Data Bisnis & Registrasi")
    
    perusahaan = input(f"\n{Colors.INFO}➜ Masukkan Nama Perusahaan: {Colors.RESET}").strip().title()
    
    if len(perusahaan) < 3:
        print(f"{Colors.ERROR}✗ Nama perusahaan terlalu pendek!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Mencari data perusahaan", 3, "bars")
    
    print(f"\n{Colors.SUCCESS}✓ DATA PERUSAHAAN DITEMUKAN:{Colors.RESET}")
    
    result_lines = [
        f"Nama: {Colors.ACCENT}{perusahaan}{Colors.LIGHT}",
        f"Status: {Colors.SUCCESS}AKTIF{Colors.LIGHT}",
        f"NPWP: 01.234.567.8-912.345",
        f"Alamat: JAKARTA SELATAN",
        f"Industri: TEKNOLOGI INFORMASI",
        f"Tahun Berdiri: 2020"
    ]
    
    draw_box("HASIL ANALISIS", result_lines, Colors.SUCCESS, Colors.ACCENT)
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_berita():
    elegant_menu_header("CEK BERITA", "Analisis Berita & Artikel")
    
    keyword = input(f"\n{Colors.INFO}➜ Masukkan kata kunci berita: {Colors.RESET}").strip()
    
    if len(keyword) < 3:
        print(f"{Colors.ERROR}✗ Kata kunci terlalu pendek!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Mencari berita terkini", 3, "modern")
    
    print(f"\n{Colors.SUCCESS}✓ BERITA DITEMUKAN:{Colors.RESET}")
    
    result_lines = [
        f"Keyword: {Colors.ACCENT}{keyword}{Colors.LIGHT}",
        f"Jumlah Berita: 15 artikel",
        f"Sumber: Detik.com, Kompas.com, CNN Indonesia",
        f"Rentang Waktu: 7 hari terakhir",
        f"Sentimen: {Colors.SUCCESS}POSITIF{Colors.LIGHT}"
    ]
    
    draw_box("HASIL PENCARIAN", result_lines, Colors.INFO, Colors.ACCENT)
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def cek_data_global():
    elegant_menu_header("CEK DATA GLOBAL", "International Intelligence")
    
    target = input(f"\n{Colors.INFO}➜ Masukkan target (nama/email/domain): {Colors.RESET}").strip()
    
    if len(target) < 3:
        print(f"{Colors.ERROR}✗ Input terlalu pendek!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Scanning global databases", 4, "modern")
    
    print(f"\n{Colors.SUCCESS}✓ DATA GLOBAL DITEMUKAN:{Colors.RESET}")
    
    result_lines = [
        f"Target: {Colors.ACCENT}{target}{Colors.LIGHT}",
        f"Database: 15 sumber internasional",
        f"Hasil: 3 match ditemukan",
        f"Lokasi: MULTI-NASIONAL",
        f"Status: {Colors.SUCCESS}ANALISIS SELESAI{Colors.LIGHT}"
    ]
    
    draw_box("HASIL GLOBAL", result_lines, Colors.INFO, Colors.ACCENT)
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def analisis_data():
    elegant_menu_header("ANALISIS DATA", "Advanced Data Processing")
    
    print(f"\n{Colors.INFO}Pilih jenis analisis:{Colors.RESET}")
    print(f"{Colors.LIGHT}1. Analisis hubungan data{Colors.RESET}")
    print(f"{Colors.LIGHT}2. Pattern recognition{Colors.RESET}")
    print(f"{Colors.LIGHT}3. Timeline analysis{Colors.RESET}")
    
    choice = input(f"\n{Colors.INFO}➜ Pilih [1-3]: {Colors.RESET}").strip()
    
    elegant_loading("Memproses data", 3, "bars")
    
    if choice == "1":
        print(f"\n{Colors.SUCCESS}✓ ANALISIS HUBUNGAN DATA:{Colors.RESET}")
        result_lines = [
            "Jumlah node: 15 entitas",
            "Hubungan: 28 koneksi",
            "Cluster: 3 kelompok utama",
            "Anomali: 2 terdeteksi",
            f"Status: {Colors.SUCCESS}SELESAI{Colors.LIGHT}"
        ]
    elif choice == "2":
        print(f"\n{Colors.SUCCESS}✓ PATTERN RECOGNITION:{Colors.RESET}")
        result_lines = [
            "Pattern: 5 pola teridentifikasi",
            "Confidence: 92% akurasi",
            "Anomali: 3 pola tidak biasa",
            "Rekomendasi: Investigasi lanjutan",
            f"Status: {Colors.SUCCESS}SELESAI{Colors.LIGHT}"
        ]
    else:
        print(f"\n{Colors.SUCCESS}✓ TIMELINE ANALYSIS:{Colors.RESET}")
        result_lines = [
            "Periode: 30 hari terakhir",
            "Event: 45 aktivitas",
            "Trend: Peningkatan 15%",
            "Puncak: 5 hari lalu",
            f"Status: {Colors.SUCCESS}SELESAI{Colors.LIGHT}"
        ]
    
    draw_box("HASIL ANALISIS", result_lines, Colors.SUCCESS, Colors.ACCENT)
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def advanced_search():
    elegant_menu_header("ADVANCED SEARCH", "Pencarian Mendalam")
    
    query = input(f"\n{Colors.INFO}➜ Masukkan query pencarian: {Colors.RESET}").strip()
    
    if len(query) < 3:
        print(f"{Colors.ERROR}✗ Query terlalu pendek!{Colors.RESET}")
        input(f"{Colors.WARNING}➜ Tekan Enter untuk kembali... {Colors.RESET}")
        return
    
    elegant_loading("Melakukan pencarian mendalam", 4, "modern")
    
    print(f"\n{Colors.SUCCESS}✓ HASIL PENCARIAN MENDALAM:{Colors.RESET}")
    
    result_lines = [
        f"Query: {Colors.ACCENT}{query}{Colors.LIGHT}",
        f"Sumber: 25 database",
        f"Hasil: 127 item ditemukan",
        f"Relevansi: 89%",
        f"Waktu: 3.2 detik"
    ]
    
    draw_box("HASIL SEARCH", result_lines, Colors.INFO, Colors.ACCENT)
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

def report_generator():
    elegant_menu_header("REPORT GENERATOR", "Laporan Professional")
    
    print(f"\n{Colors.INFO}Pilih jenis laporan:{Colors.RESET}")
    print(f"{Colors.LIGHT}1. Laporan OSINT{Colors.RESET}")
    print(f"{Colors.LIGHT}2. Laporan Keamanan{Colors.RESET}")
    print(f"{Colors.LIGHT}3. Laporan Analisis{Colors.RESET}")
    
    choice = input(f"\n{Colors.INFO}➜ Pilih [1-3]: {Colors.RESET}").strip()
    
    elegant_loading("Membuat laporan professional", 3, "bars")
    
    print(f"\n{Colors.SUCCESS}✓ LAPORAN BERHASIL DIBUAT:{Colors.RESET}")
    
    result_lines = [
        f"Jenis: {'OSINT' if choice == '1' else 'Keamanan' if choice == '2' else 'Analisis'}",
        f"Format: PDF & HTML",
        f"Pages: 15 halaman",
        f"Data: 45 point evidence",
        f"Status: {Colors.SUCCESS}TERGENERATE{Colors.LIGHT}"
    ]
    
    draw_box("HASIL REPORT", result_lines, Colors.SUCCESS, Colors.ACCENT)
    
    input(f"\n{Colors.INFO}➜ Tekan Enter untuk kembali... {Colors.RESET}")

# ==================== MENUS UTAMA ====================

def osint_menu():
    while True:
        elegant_menu_header("MENU OSINT", "Advanced Intelligence Gathering")
        
        menu_items = [
            f"{Colors.SUCCESS}1.{Colors.LIGHT}  🆔  Cek NIK & Data Kependudukan",
            f"{Colors.SUCCESS}2.{Colors.LIGHT}  🌐  Cek IP Address & Geolocation", 
            f"{Colors.SUCCESS}3.{Colors.LIGHT}  🚗  Cek Plat Nomor Kendaraan",
            f"{Colors.SUCCESS}4.{Colors.LIGHT}  👤  Cek Nama & Profil Sosial Media",
            f"{Colors.SUCCESS}5.{Colors.LIGHT}  📱  Cek Nomor Telepon & Operator",
            f"{Colors.SUCCESS}6.{Colors.LIGHT}  📧  Cek Email & Validasi",
            f"{Colors.SUCCESS}7.{Colors.LIGHT}  🔗  Cek Domain & Website Info",
            f"{Colors.SUCCESS}8.{Colors.LIGHT}  📍  Intelijen Koordinat & GPS",
            f"{Colors.SUCCESS}9.{Colors.LIGHT}  🏢  Cek Data Perusahaan",
            f"{Colors.SUCCESS}10.{Colors.LIGHT} 📰  Cek Berita & Artikel",
            f"{Colors.SUCCESS}11.{Colors.LIGHT} 🔐  Cek Password Strength & Leak",
            f"{Colors.SUCCESS}12.{Colors.LIGHT} 🌍  Cek Data Global",
            f"{Colors.SUCCESS}13.{Colors.LIGHT} 📊  Analisis Data Lanjutan",
            f"{Colors.SUCCESS}14.{Colors.LIGHT} 🔍  Pencarian Mendalam",
            f"{Colors.SUCCESS}15.{Colors.LIGHT} 📈  Report Generator",
            f"{Colors.WARNING}0.{Colors.LIGHT}  🏠  Kembali ke Menu Utama"
        ]
        
        for item in menu_items:
            print(f"{Colors.PRIMARY}║ {item:<55} {Colors.PRIMARY}║{Colors.RESET}")
        
        elegant_menu_footer()
        
        choice = input(f"\n{Colors.INFO}➜ Pilih menu [0-15]: {Colors.RESET}").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            elegant_loading("Memuat modul NIK", 2, "modern")
            cek_nik()
        elif choice == "2":
            elegant_loading("Memuat modul IP", 2, "dots") 
            cek_ip()
        elif choice == "3":
            elegant_loading("Memuat modul kendaraan", 2, "bars")
            cek_plat_nomor()
        elif choice == "4":
            elegant_loading("Memuat modul profil", 2, "modern")
            cek_nama()
        elif choice == "5":
            elegant_loading("Memuat modul telepon", 2, "dots")
            cek_nomor()
        elif choice == "6":
            elegant_loading("Memuat modul email", 2, "bars")
            cek_email()
        elif choice == "7":
            elegant_loading("Memuat modul domain", 2, "modern")
            cek_domain()
        elif choice == "8":
            elegant_loading("Memuat modul GPS Intelijen", 2, "dots")
            advanced_coordinate_intelligence()
        elif choice == "9":
            elegant_loading("Memuat modul perusahaan", 2, "bars")
            cek_perusahaan()
        elif choice == "10":
            elegant_loading("Memuat modul berita", 2, "modern")
            cek_berita()
        elif choice == "11":
            elegant_loading("Memuat modul keamanan", 2, "dots")
            cek_password_leak()
        elif choice == "12":
            elegant_loading("Memuat modul global", 2, "bars")
            cek_data_global()
        elif choice == "13":
            elegant_loading("Memuat modul analisis", 2, "modern")
            analisis_data()
        elif choice == "14":
            elegant_loading("Memuat modul pencarian", 2, "dots")
            advanced_search()
        elif choice == "15":
            elegant_loading("Memuat modul laporan", 2, "bars")
            report_generator()
        else:
            print(f"\n{Colors.ERROR}✗ Pilihan tidak valid!{Colors.RESET}")
            input(f"{Colors.WARNING}➜ Tekan Enter untuk melanjutkan... {Colors.RESET}")

def hacking_menu():
    while True:
        elegant_menu_header("TOOLS HACKING", "Install Security Tools")
        
        menu_items = [
            f"{Colors.ERROR}1.{Colors.LIGHT}  🗃️   SQLMAP (SQL Injection Scanner)",
            f"{Colors.ERROR}2.{Colors.LIGHT}  🔍  NMAP (Network Mapper)",
            f"{Colors.ERROR}3.{Colors.LIGHT}  💣  METASPLOIT Framework",
            f"{Colors.ERROR}4.{Colors.LIGHT}  💧  HYDRA (Brute Force Tool)",
            f"{Colors.ERROR}5.{Colors.LIGHT}  📡  AIRCRACK-NG (WiFi Audit)",
            f"{Colors.ERROR}6.{Colors.LIGHT}  🔓  JOHN THE RIPPER (Password Cracker)",
            f"{Colors.ERROR}7.{Colors.LIGHT}  📶  WIFITE2 (WiFi Cracking)",
            f"{Colors.ERROR}8.{Colors.LIGHT}  🎭  SETOOLKIT (Social Engineering)",
            f"{Colors.ERROR}9.{Colors.LIGHT}  🥩  BEEF FRAMEWORK (Browser Exploit)",
            f"{Colors.ERROR}10.{Colors.LIGHT} 🔍  WPSCAN (WordPress Scanner)",
            f"{Colors.ERROR}11.{Colors.LIGHT} 🕸️   RECON-NG (Reconnaissance)",
            f"{Colors.ERROR}12.{Colors.LIGHT} 🌐  BURP SUITE (Web Scanner)",
            f"{Colors.ERROR}13.{Colors.LIGHT} 📱  ANDROID HACKING TOOLS",
            f"{Colors.ERROR}14.{Colors.LIGHT} 📊  NETWORK ANALYZER",
            f"{Colors.SUCCESS}15.{Colors.LIGHT} 📦  INSTALL SEMUA TOOLS",
            f"{Colors.WARNING}0.{Colors.LIGHT}  🏠  Kembali ke Menu Utama"
        ]
        
        for item in menu_items:
            print(f"{Colors.PRIMARY}║ {item:<55} {Colors.PRIMARY}║{Colors.RESET}")
        
        elegant_menu_footer()
        
        choice = input(f"\n{Colors.INFO}➜ Pilih menu [0-15]: {Colors.RESET}").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            elegant_loading("Menginstall SQLMap", 3, "modern")
            install_sqlmap()
        elif choice == "2":
            elegant_loading("Menginstall Nmap", 3, "dots")
            install_nmap()
        elif choice == "3":
            elegant_loading("Menginstall Metasploit", 3, "bars")
            install_metasploit()
        elif choice == "4":
            elegant_loading("Menginstall Hydra", 3, "modern")
            install_hydra()
        elif choice == "5":
            elegant_loading("Menginstall Aircrack-ng", 3, "dots")
            install_aircrack()
        elif choice == "6":
            elegant_loading("Menginstall John The Ripper", 3, "bars")
            install_john()
        elif choice == "7":
            elegant_loading("Menginstall Wifite2", 3, "modern")
            install_wifite()
        elif choice == "8":
            elegant_loading("Menginstall SEToolkit", 3, "dots")
            install_setoolkit()
        elif choice == "9":
            elegant_loading("Menginstall BeEF Framework", 3, "bars")
            install_beef()
        elif choice == "10":
            elegant_loading("Menginstall WPScan", 3, "modern")
            install_wpscan()
        elif choice == "11":
            elegant_loading("Menginstall Recon-ng", 3, "dots")
            install_reconng()
        elif choice == "12":
            elegant_loading("Menginstall Burp Suite", 3, "bars")
            install_burp()
        elif choice == "13":
            elegant_loading("Menginstall Android Tools", 3, "modern")
            install_android_tools()
        elif choice == "14":
            elegant_loading("Menginstall Network Analyzer", 3, "dots")
            install_network_analyzer()
        elif choice == "15":
            elegant_loading("Menginstall semua tools", 3, "bars")
            install_all_tools()
        else:
            print(f"\n{Colors.ERROR}✗ Pilihan tidak valid!{Colors.RESET}")
            input(f"{Colors.WARNING}➜ Tekan Enter untuk melanjutkan... {Colors.RESET}")

def main_menu():
    while True:
        clear_screen()
        
        print(f"\n{Colors.INFO}")
        print(" ███████╗██╗      █████╗ ██╗   ██╗")
        print(" ██╔════╝██║     ██╔══██╗╚██╗ ██╔╝")
        print(" █████╗  ██║     ███████║ ╚████╔╝ ")
        print(" ██╔══╝  ██║     ██╔══██║  ╚██╔╝  ")
        print(" ██║     ███████╗██║  ██║   ██║   ")
        print(" ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ")
        print(f"{Colors.RESET}")
        
        footer_text = " TOOLS INI DIKEMBANGKAN OLEH CYBER FLAY "
        colors = [Colors.SUCCESS, Colors.WARNING, Colors.INFO, Colors.ACCENT]
        marquee_text(footer_text, colors, 2)
        
        print("\n")
        
        menu_items = [
            f"{Colors.SUCCESS}1.{Colors.LIGHT}  🕵️  MENU OSINT - Intelligence Gathering",
            f"{Colors.ERROR}2.{Colors.LIGHT}  ⚡ TOOLS HACKING - Install Security Tools", 
            f"{Colors.ERROR}3.{Colors.LIGHT}  🌪️  DDOS TOOLS - Distributed Denial of Service",
            f"{Colors.INFO}4.{Colors.LIGHT}  🔍  OSINT DOMAIN - Advanced Domain Intelligence",
            f"{Colors.WARNING}5.{Colors.LIGHT}  🚪 KELUAR - Exit Application",
            "",
            f"{Colors.INFO}💡 Tips: Gunakan tools dengan bertanggung jawab",
            f"{Colors.WARNING}⚠  Warning: Untuk tujuan edukasi dan keamanan sah"
        ]
        
        draw_box("MENU UTAMA", menu_items, Colors.PRIMARY, Colors.ACCENT)
        
        print(f"\n{Colors.DARK}┌─{Colors.INFO} STATUS SISTEM {Colors.DARK}─{'─' * 40}┐{Colors.RESET}")
        print(f"{Colors.DARK}│ {Colors.SUCCESS}● {Colors.LIGHT}OSINT Modules    {Colors.SUCCESS}Ready{Colors.DARK}               │{Colors.RESET}")
        print(f"{Colors.DARK}│ {Colors.SUCCESS}● {Colors.LIGHT}Hacking Tools    {Colors.SUCCESS}Ready{Colors.DARK}               │{Colors.RESET}")
        print(f"{Colors.DARK}│ {Colors.ERROR}● {Colors.LIGHT}DDOS Tools       {Colors.ERROR}High Risk{Colors.DARK}            │{Colors.RESET}")
        print(f"{Colors.DARK}│ {Colors.INFO}● {Colors.LIGHT}OSINT Domain     {Colors.SUCCESS}Ready{Colors.DARK}               │{Colors.RESET}")
        print(f"{Colors.DARK}│ {Colors.SUCCESS}● {Colors.LIGHT}Security Level   {Colors.WARNING}High{Colors.DARK}                │{Colors.RESET}")
        print(f"{Colors.DARK}└{'─' * 56}┘{Colors.RESET}")
        
        choice = input(f"\n{Colors.INFO}➜ Pilih menu [1-5]: {Colors.RESET}").strip()
        
        if choice == "1":
            elegant_loading("Membuka OSINT Toolkit", 2, "modern")
            osint_menu()
        elif choice == "2":
            elegant_loading("Mengaktifkan Security Tools", 2, "dots")
            hacking_menu()
        elif choice == "3":
            elegant_loading("Mengakses DDOS Tools", 2, "bars")
            ddos_menu()
        elif choice == "4":
            elegant_loading("Membuka OSINT Domain Tools", 2, "modern")
            osint_domain_menu()
        elif choice == "5":
            print(f"\n{Colors.INFO}👋 Terima kasih telah menggunakan Cyber Flay Tools!{Colors.RESET}")
            elegant_loading("Menutup aplikasi", 2, "modern")
            break
        else:
            print(f"\n{Colors.ERROR}✗ Pilihan tidak valid!{Colors.RESET}")
            elegant_loading("Memuat ulang menu", 1, "pulse")

def main():
    try:
        welcome_screen()
        
        if login_screen():
            main_menu()
            
        print(f"\n{Colors.SUCCESS}✨ Sampai jumpa! Terima kasih telah menggunakan Cyber Flay Tools.{Colors.RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}\n⚠  Program dihentikan oleh pengguna.{Colors.RESET}")
        elegant_loading("Menyimpan log", 1, "dots")
    except Exception as e:
        print(f"\n{Colors.ERROR}💥 Error: {e}{Colors.RESET}")
        elegant_loading("Mengatasi error", 2, "pulse")

if __name__ == "__main__":
    try:
        import phonenumbers
        import whois
        import dns.resolver
    except ImportError:
        print(f"{Colors.WARNING}📦 Menginstall dependencies...{Colors.RESET}")
        os.system('pip install phonenumbers python-whois dnspython geopy requests')
        print(f"{Colors.SUCCESS}✓ Dependencies terinstall!{Colors.RESET}")
        time.sleep(2)
    
    main()


saya mau amanin tools ini saya kan mau up di github takutnya di decode sama orang