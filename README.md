# Automated Ping-Pong Machine 🏓

An automated ping-pong playing machine powered by computer vision and live control algorithms. The system uses OpenCV for precise ball tracking and Raspberry Pi for video feed analysis, color-based object detection, and motor control.

<img width="357" height="241" alt="automated_ping_pong_machine" src="https://github.com/user-attachments/assets/7147d212-e98f-4d33-b604-1a3089570032" />

## Demo
Watch the machine in action here:

https://github.com/user-attachments/assets/d2a08113-af3e-416e-847a-7ed33282a2de

https://github.com/user-attachments/assets/6efa010e-5009-4735-9f6e-56ba73a79410

## Project Overview
- Tracks a moving ping-pong ball using OpenCV color detection
- Computes ball position in real time from camera input
- Controls DC motors to dynamically position the paddle
- Runs on a Raspberry Pi for vision processing and motion control

## Tech Stack
- **Python**
- **OpenCV**
- **Raspberry Pi**
- **Raspberry Pi Camera Module**
- **DC Motors & Motor Driver**

## Setup

### Running on Raspberry Pi

**On the Raspberry Pi:**
1. Start the hotspot
2. Run `sudo raspi-config` if needed for initial configuration
3. Find the Pi's IP address:
```bash
   hostname -I
```

**On your computer:**
1. Connect to the Pi's hotspot
2. SSH into the Pi:
```bash
   ssh <username>@<IP_ADDRESS>
``` 
  (Type `yes` if prompted on first connection)

3. Enter your password when prompted

