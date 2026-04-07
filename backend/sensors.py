import os
import random
import time


def _is_pi():
    try:
        with open("/proc/cpuinfo") as f:
            return "Raspberry Pi" in f.read()
    except:
        return False


ON_PI = _is_pi()

if ON_PI:
    try:
        import board
        import busio
        import adafruit_bme680
        import adafruit_scd4x
        _i2c = busio.I2C(board.SCL, board.SDA)
        _bme = adafruit_bme680.Adafruit_BME680_I2C(_i2c)
        _scd = adafruit_scd4x.SCD4X(_i2c)
        _scd.start_periodic_measurement()
        SENSORS_REAL = True
    except Exception as e:
        print(f"[sensors] {e}, falling back to mock")
        SENSORS_REAL = False
else:
    SENSORS_REAL = False


def _mock():
    t = time.time()
    return {
        "temperature": round(21.0 + 1.5 * (0.5 - abs((t % 60) / 60 - 0.5)), 1),
        "humidity": round(55 + 8 * random.uniform(-1, 1), 1),
        "pressure": round(1013.2 + random.uniform(-0.5, 0.5), 1),
        "voc_index": round(120 + random.randint(-20, 20)),
        "co2": round(720 + random.randint(-40, 80)),
        "aqi": 42,
        "pm25": round(8 + random.uniform(-2, 2), 1),
        "source": "mock",
    }


def _real():
    data = {
        "temperature": round(_bme.temperature, 1),
        "humidity": round(_bme.relative_humidity, 1),
        "pressure": round(_bme.pressure, 1),
        "voc_index": round(_bme.gas),
        "co2": None,
        "aqi": None,
        "pm25": None,
        "source": "real",
    }
    if _scd.data_ready:
        data["co2"] = _scd.CO2
    return data


def get_sensors():
    if SENSORS_REAL:
        try:
            return _real()
        except Exception as e:
            print(f"[sensors] {e}")
    return _mock()
