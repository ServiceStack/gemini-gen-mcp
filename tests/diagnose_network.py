import socket
import time
import requests

def diagnostic():
    host = "generativelanguage.googleapis.com"
    print(f"Diagnosing connectivity to {host}...")

    # Test DNS resolution
    try:
        start = time.time()
        info = socket.getaddrinfo(host, 443)
        duration = time.time() - start
        print(f"DNS Resolution took {duration:.4f}s")
        for res in info:
            print(f"  - Family: {res[0]}, Address: {res[4][0]}")
    except Exception as e:
        print(f"DNS Resolution failed: {e}")

    # Test IPv4 connection
    try:
        print("\nTesting IPv4 connection...")
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        # Find first IPv4
        ip4 = next(res[4][0] for res in info if res[0] == socket.AF_INET)
        s.connect((ip4, 443))
        print(f"IPv4 connection to {ip4} took {time.time() - start:.4f}s")
        s.close()
    except Exception as e:
        print(f"IPv4 connection failed: {e}")

    # Test IPv6 connection
    try:
        print("\nTesting IPv6 connection...")
        start = time.time()
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.settimeout(5)
        # Find first IPv6
        ip6 = next(res[4][0] for res in info if res[0] == socket.AF_INET6)
        s.connect((ip6, 443))
        print(f"IPv6 connection to {ip6} took {time.time() - start:.4f}s")
        s.close()
    except Exception as e:
        print(f"IPv6 connection failed (likely the culprit if it hangs): {e}")

    # Test HTTPS via requests (often uses different logic)
    try:
        print("\nTesting HTTPS GET via requests...")
        start = time.time()
        # Just a simple health check or root hit
        r = requests.get(f"https://{host}/", timeout=10)
        print(f"HTTPS GET took {time.time() - start:.4f}s, status: {r.status_code}")
    except Exception as e:
        print(f"HTTPS GET failed: {e}")

if __name__ == "__main__":
    diagnostic()
