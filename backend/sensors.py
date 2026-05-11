import random
import time


def _is_pi():
    try:
        with open("/proc/cpuinfo") as f:
            return "Raspberry Pi" in f.read()
    except:
        return False


ON_PI = _is_pi()

_bmp = None

if ON_PI:
    try:
        from smbus2 import SMBus
        from bmp280 import BMP280
        _i2c_bus = SMBus(1)
        try:
            _bmp = BMP280(i2c_addr=0x77, i2c_dev=_i2c_bus)
            print("[sensors] BMP280 ready on bus 1, addr 0x77")
        except Exception:
            _bmp = BMP280(i2c_addr=0x76, i2c_dev=_i2c_bus)
            print("[sensors] BMP280 ready on bus 1, addr 0x76")
    except Exception as e:
        print(f"[sensors] BMP280 init failed: {e}")
        _bmp = None


def _mock():
    t = time.time()
    return {
        "temperature": round(21.0 + 1.5 * (0.5 - abs((t % 60) / 60 - 0.5)), 1),
        "humidity": round(55 + 8 * random.uniform(-1, 1), 1),
        "pressure": round(1013 + random.uniform(-2, 2), 1),
        "source": "mock",
    }


def _real():
    return {
        "temperature": round(_bmp.get_temperature(), 1),
        "humidity": None,
        "pressure": round(_bmp.get_pressure(), 1),
        "source": "real",
    }


def get_sensors():
    if _bmp is not None:
        try:
            return _real()
        except Exception as e:
            print(f"[sensors] read error: {e}")
    return _mock()
