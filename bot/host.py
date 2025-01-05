import logging
import os
import signal
import socket
import subprocess
import threading
import time

from main import run_bot

# You can change those
devices = {
    "192.168.0.107": 2,  # Phone
    "192.168.0.108": 1,  # PC
}
command_to_execute = "python3 main.py"

# You can't change those
command_thread = None


def get_current_ipv4() -> str | None:
    """Retrieve the current IPv4 address of this machine."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def is_device_reachable(ip: str) -> bool:
    """Ping a device to check if it's reachable."""
    command = ["ping", "-n" if os.name == "nt" else "-c", "1", "-W" if os.name != "nt" else "-w", "1", ip]  # Send one ping request  # Set timeout to 1 second for Unix (seconds) or Windows (milliseconds)
    response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return response.returncode == 0


def is_current_the_highest_reachable() -> bool:
    try:
        current_ip = get_current_ipv4()

        for ip, priority in devices.items():
            if ip == current_ip:
                continue

            logging.info(f"Pinging {ip}")
            if is_device_reachable(ip):
                logging.info(f"Device {ip} is reachable")
                if priority < devices[current_ip]:
                    return False
            else:
                logging.info(f"Device {ip} is not reachable")

        return True
    except Exception as e:
        return True


def main():
    global command_thread

    while True:
        time.sleep(2)
        if is_current_the_highest_reachable():
            # If current device is the highest reachable, then run the bot on the current
            if not command_thread or not command_thread.is_alive():
                command_thread = threading.Thread(target=lambda: os.system(command_to_execute), daemon=True)
                command_thread.start()
            continue

        # If there is some device that has higher priority and is reachable, stop the bot on the current
        if command_thread and command_thread.is_alive():
            command_thread = None
            logging.info("Finishing the thread")
            pgid = os.getpgrp()
            os.killpg(pgid, signal.SIGINT)


if __name__ == "__main__":
    main()
