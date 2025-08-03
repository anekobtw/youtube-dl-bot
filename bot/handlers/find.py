from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

SUBNET = "192.168.0."
TIMEOUT = 0.1


def check_health(ip):
    url = f"http://{ip}:8000/health"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        if r.status_code == 200 and r.json().get("status") == "ok":
            return ip
    except Exception:
        pass

    return None


def find() -> str | None:
    ips = [f"{SUBNET}{i}" for i in range(1, 255)]

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_health, ip): ip for ip in ips}
        for future in as_completed(futures):
            result = future.result()
            if result:
                return result

    return None
