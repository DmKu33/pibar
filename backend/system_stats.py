import shutil
import socket
import time

_start = time.time()


def get_system():
    uptime_s = int(time.time() - _start)
    d, rem = divmod(uptime_s, 86400)
    h, rem = divmod(rem, 3600)
    m = rem // 60
    uptime = f"{d}d {h}h {m}m" if d else f"{h}h {m}m"

    temp = None
    for path in [
        "/sys/class/thermal/thermal_zone0/temp",
        "/sys/class/hwmon/hwmon0/temp1_input",
    ]:
        try:
            with open(path) as f:
                temp = round(int(f.read().strip()) / 1000, 1)
            break
        except:
            pass

    total, used, free = shutil.disk_usage("/")
    disk_free_gb = round(free / 1e9, 1)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
        connected = True
    except:
        ip = "—"
        connected = False

    return {
        "uptime": uptime,
        "cpu_temp": temp,
        "disk_free_gb": disk_free_gb,
        "ip": ip,
        "connected": connected,
    }
