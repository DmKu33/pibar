# pibar

Desk dashboard on a 6.9" 1280x480 ultrawide bar display driven by a Raspberry Pi 3. Sits under a main monitor. Shows room temperature, barometric pressure, reminders, and system stats. Reminders are added via Telegram bot.

## Stack

- Flask backend serving sensor data and tasks as JSON
- Single HTML page polled every 6s, rendered in Chromium kiosk mode
- BMP280 barometer via Grove Base Hat (I2C bus 1, addr 0x77)
- Telegram bot writes reminders to `tasks.md`

## Run

```bash
cp .env.example .env  # fill in TELEGRAM_TOKEN and TELEGRAM_OWNER_ID
bash run.sh
```

## Structure

```
backend/      Flask app, sensors, bot, tasks parser
frontend/     dashboard UI (single HTML file)
cad/          OpenSCAD enclosure model + STL exports
forge/        ForgeCAD enclosure (JavaScript + STL)
docs/         devlog and project documentation
pibar_imgs/   photos, screenshots, renders
```

## Hardware

- Raspberry Pi 3 Model B
- 6.9" 1280x480 IPS bar screen + HDMI-to-MIPI driver board
- Grove Base Hat for Raspberry Pi
- BMP280 barometer sensor
