# Yocto Linux for Raspberry Pi 5 - AI Plant Monitor

Custom embedded Linux distribution built with Yocto Project for AI-powered plant monitoring system.

![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205-c51a4a)
![Yocto](https://img.shields.io/badge/Yocto-Kirkstone-green)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Hardware Requirements](#hardware-requirements)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Building the Image](#building-the-image)
- [Flashing to SD Card](#flashing-to-sd-card)
- [First Boot Setup](#first-boot-setup)
- [What's Included](#whats-included)
- [Custom Layers](#custom-layers)
- [Device Tree Overlays](#device-tree-overlays)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project creates a minimal, optimized Linux distribution for the Raspberry Pi 5, specifically tailored for running an AI-powered plant monitoring system with:

- Multi-sensor support (I2C, SPI)
- TensorFlow Lite integration
- Automated watering control
- OLED display interface
- WiFi networking
- Email notifications

**Key Features:**
- ✅ Custom device tree overlays for I2C and SPI
- ✅ Python 3.10 with scientific libraries
- ✅ TensorFlow Lite Runtime
- ✅ Systemd init system
- ✅ WiFi and network tools
- ✅ Minimal footprint (~500MB image)

---

## 🔧 Hardware Requirements

### Development Machine
- **OS:** Ubuntu 20.04+ or macOS with Ubuntu VM
- **RAM:** 8GB minimum, 16GB recommended
- **Disk:** 100GB free space
- **CPU:** Multi-core recommended (build uses all cores)

### Target Device
- **Raspberry Pi 5** (4GB or 8GB RAM)
- **MicroSD Card:** 32GB minimum, Class 10
- **Power Supply:** Official 5V 5A USB-C adapter

### Peripherals (for Plant Monitor)
- BME280 (I2C - Temperature/Humidity)
- BH1750 (I2C - Light sensor)
- SSD1306 OLED (I2C - 128x64 display)
- MCP3008 (SPI - ADC for soil sensor)
- Capacitive soil moisture sensor
- 5V relay module + water pump

---

## 📦 Prerequisites

### Install Build Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y gawk wget git diffstat unzip texinfo gcc build-essential \
  chrpath socat cpio python3 python3-pip python3-pexpect xz-utils \
  debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa \
  libsdl1.2-dev pylint xterm python3-subunit mesa-common-dev zstd \
  liblz4-tool file locales libacl1

sudo locale-gen en_US.UTF-8
```

**macOS (via Ubuntu VM):**
- Install VirtualBox or UTM
- Create Ubuntu 22.04 VM with 50GB+ disk
- Follow Ubuntu instructions above

---

## 📁 Project Structure
```
yocto-ai-project/
├── poky/                           # Yocto core (cloned from git)
├── meta-raspberrypi/               # Raspberry Pi BSP layer
├── meta-openembedded/              # Additional recipes
│   ├── meta-oe/
│   ├── meta-python/
│   └── meta-networking/
├── meta-homeai/                    # Custom layer (our recipes)
│   ├── conf/
│   │   └── layer.conf
│   ├── recipes-kernel/
│   │   └── linux/
│   │       └── linux-raspberrypi/
│   │           └── homeai-overlay.dts  # Device tree overlay
│   └── recipes-core/
│       └── images/
│           └── homeai-image.bb     # Custom image recipe
└── build-rpi5/                     # Build directory
    ├── conf/
    │   ├── local.conf              # Build configuration
    │   └── bblayers.conf           # Layer configuration
    └── tmp/
        └── deploy/
            └── images/
                └── raspberrypi5/   # Built images here!
```

---

## 🏗️ Building the Image

### Step 1: Clone Yocto Repositories
```bash
# Create project directory
mkdir -p ~/Documents/Yocto/yocto-ai-project
cd ~/Documents/Yocto/yocto-ai-project

# Clone Poky (Yocto core) - Kirkstone branch
git clone -b kirkstone git://git.yoctoproject.org/poky.git

# Clone Raspberry Pi BSP layer
git clone -b kirkstone https://github.com/agherzan/meta-raspberrypi.git

# Clone OpenEmbedded layers
git clone -b kirkstone https://github.com/openembedded/meta-openembedded.git
```

---

### Step 2: Initialize Build Environment
```bash
cd ~/Documents/Yocto/yocto-ai-project
source poky/oe-init-build-env build-rpi5
```

**This creates and enters the `build-rpi5/` directory.**

---

### Step 3: Configure Build (local.conf)
```bash
nano conf/local.conf
```

**Add/modify these settings:**
```bash
# Target machine
MACHINE = "raspberrypi5"

# Systemd init system
DISTRO_FEATURES:append = " systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"
DISTRO_FEATURES_BACKFILL_CONSIDERED = "sysvinit"
VIRTUAL-RUNTIME_initscripts = ""

# Enable UART for serial console
ENABLE_UART = "1"

# Optimize build (adjust based on your CPU cores)
BB_NUMBER_THREADS = "9"
PARALLEL_MAKE = "-j 9"

# WiFi support
IMAGE_INSTALL:append = " \
    linux-firmware-rpidistro-bcm43455 \
    wpa-supplicant \
    iw \
    wireless-tools \
"

# Core packages
IMAGE_INSTALL:append = " \
    python3 \
    python3-pip \
    python3-numpy \
    python3-pillow \
    nano \
    htop \
    i2c-tools \
    spidev \
    libgpiod \
    libgpiod-tools \
"

# TensorFlow Lite Runtime
IMAGE_INSTALL:append = " \
    tflite-runtime \
"
```

---

### Step 4: Configure Layers (bblayers.conf)
```bash
nano conf/bblayers.conf
```

**Set BBLAYERS to:**
```python
BBLAYERS ?= " \
  /home/YOUR_USERNAME/Documents/Yocto/yocto-ai-project/poky/meta \
  /home/YOUR_USERNAME/Documents/Yocto/yocto-ai-project/poky/meta-poky \
  /home/YOUR_USERNAME/Documents/Yocto/yocto-ai-project/poky/meta-yocto-bsp \
  /home/YOUR_USERNAME/Documents/Yocto/yocto-ai-project/meta-raspberrypi \
  /home/YOUR_USERNAME/Documents/Yocto/yocto-ai-project/meta-openembedded/meta-oe \
  /home/YOUR_USERNAME/Documents/Yocto/yocto-ai-project/meta-openembedded/meta-python \
  /home/YOUR_USERNAME/Documents/Yocto/yocto-ai-project/meta-openembedded/meta-networking \
  "
```

**⚠️ Replace `/home/YOUR_USERNAME/` with your actual path!**

**Verify layers:**
```bash
bitbake-layers show-layers
```

---

### Step 5: Build the Image
```bash
bitbake core-image-base
```

**Build time:**
- First build: 3-6 hours
- Subsequent builds: 30 minutes - 2 hours (cached)

**Output location:**
```
build-rpi5/tmp/deploy/images/raspberrypi5/
└── core-image-base-raspberrypi5.wic.bz2
```

---

### Step 6: Decompress Image
```bash
cd ~/Documents/Yocto/yocto-ai-project/build-rpi5/tmp/deploy/images/raspberrypi5/

bzcat core-image-base-raspberrypi5.wic.bz2 > rpi5-image.wic
```

---

## 💾 Flashing to SD Card

### On macOS
```bash
# Find SD card
diskutil list
# Look for your SD card (usually /dev/disk4 or /dev/disk5)

# Unmount (don't eject!)
diskutil unmountDisk /dev/disk4

# Flash image (use rdisk for faster write)
sudo dd if=~/Documents/Yocto/yocto-ai-project/build-rpi5/tmp/deploy/images/raspberrypi5/rpi5-image.wic \
        of=/dev/rdisk4 bs=4m status=progress

# Sync and eject
sync
diskutil eject /dev/disk4
```

### On Linux
```bash
# Find SD card
lsblk

# Unmount
sudo umount /dev/sdX*

# Flash
sudo dd if=rpi5-image.wic of=/dev/sdX bs=4M status=progress

# Sync
sync
```

**⚠️ WARNING: Double-check disk number! `dd` will erase everything on the target disk.**

---

## 🚀 First Boot Setup

### 1. Insert SD Card and Boot

- Insert SD card into Raspberry Pi 5
- Connect Ethernet cable (or configure WiFi later)
- Connect power
- Wait ~30 seconds for boot

### 2. Find IP Address

**Option A: Check router's DHCP leases**

**Option B: Scan network**
```bash
nmap -sn 192.168.1.0/24 | grep -B 2 "Raspberry"
```

**Option C: Connect via serial console** (if UART enabled)

### 3. SSH into Pi
```bash
# Remove old SSH key if reflashing
ssh-keygen -R <PI_IP_ADDRESS>

# Connect (default: no password)
ssh root@<PI_IP_ADDRESS>
```

**Default credentials:**
- Username: `root`
- Password: (none - direct login)

---

## 📦 What's Included

### Core System
- **Kernel:** Linux 6.6.x with Raspberry Pi patches
- **Init:** systemd
- **Shell:** bash
- **Package Manager:** opkg

### Development Tools
- Python 3.10
- pip (Python package manager)
- nano (text editor)
- htop (process monitor)
- git

### Hardware Support
- **I2C:** i2c-tools, /dev/i2c-1
- **SPI:** spidev, /dev/spidev0.0
- **GPIO:** libgpiod, gpioset/gpioget

### Network
- WiFi firmware (BCM43455)
- wpa_supplicant
- SSH server (dropbear)
- Network tools (ping, ip, ifconfig)

### AI/ML
- TensorFlow Lite Runtime
- NumPy
- Pillow (PIL)

---

## 🔧 Custom Layers

### meta-homeai Layer

**Purpose:** Custom recipes for plant monitoring system

**Location:** `meta-homeai/`

**Includes:**
- Device tree overlays (I2C, SPI, GPIO configuration)
- Custom image recipes
- Application packages

**To add to build:**

1. Create layer:
```bash
bitbake-layers create-layer meta-homeai
```

2. Add to bblayers.conf:
```bash
bitbake-layers add-layer ../meta-homeai
```

---

## 🌳 Device Tree Overlays

### homeai-overlay.dts

**Purpose:** Enable I2C and SPI interfaces for sensors

**Features:**
- I2C bus 1 enabled (GPIO 2/3)
- SPI0 enabled (GPIO 7-11)
- GPIO 17 configured for relay control

**Location:**
```
meta-homeai/recipes-kernel/linux/linux-raspberrypi/homeai-overlay.dts
```

**How it works:**
```
.dts file → compiled to .dtbo → installed to /boot/overlays/
                                           ↓
                                    config.txt loads it
                                           ↓
                                    Kernel enables I2C/SPI
```

**Verify overlay is loaded:**
```bash
# On the Pi
ls /boot/overlays/ | grep homeai
cat /boot/config.txt | grep dtoverlay
```

---

## 🔍 Troubleshooting

### Build Fails

**Problem:** `ERROR: Nothing PROVIDES 'xyz'`

**Solution:**
```bash
# Check if layer providing 'xyz' is added
bitbake-layers show-layers

# Search for recipe
bitbake-layers show-recipes | grep xyz
```

---

**Problem:** Disk space issues

**Solution:**
```bash
# Clean build artifacts
bitbake -c cleanall <recipe-name>

# Or clean entire build
rm -rf tmp/
```

---

### SD Card Won't Boot

**Check:**
1. SD card properly flashed? Try re-flashing
2. Power supply adequate? (5V 5A required)
3. HDMI connected? (check for boot messages)
4. UART console? (connect serial adapter)

---

### I2C/SPI Not Working

**Verify device tree overlay:**
```bash
ls /boot/overlays/ | grep homeai
cat /boot/config.txt | grep dtoverlay
```

**Check devices exist:**
```bash
ls /dev/i2c*   # Should show /dev/i2c-1
ls /dev/spi*   # Should show /dev/spidev0.0
```

**Test I2C:**
```bash
i2cdetect -y 1
```

---

### WiFi Not Connecting

**Check firmware installed:**
```bash
ls /lib/firmware/brcm/ | grep bcm43455
```

**Configure WiFi:**
```bash
wpa_passphrase "SSID" "password" > /etc/wpa_supplicant/wpa_supplicant.conf
wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
dhclient wlan0
```

---

## 📚 Useful Commands

### Yocto Build
```bash
# Initialize build environment
source poky/oe-init-build-env build-rpi5

# Build image
bitbake core-image-base

# Clean a recipe
bitbake -c cleanall <recipe-name>

# Show layers
bitbake-layers show-layers

# Show recipes
bitbake-layers show-recipes

# Find recipe providing a package
oe-pkgdata-util find-path /usr/bin/python3
```

### On Raspberry Pi
```bash
# I2C
i2cdetect -y 1
i2cget -y 1 0x76 0xD0  # Read from BME280

# SPI
ls /dev/spidev*

# GPIO
gpioinfo
gpioset gpiochip4 17=1  # Set GPIO 17 high
gpioget gpiochip4 17    # Read GPIO 17

# Network
ip addr show
iwconfig
wpa_cli status

# System
systemctl status
journalctl -f
htop
```

---

## 🔗 Related Projects

- **Plant Monitor Application:** [plant-monitor repository](https://github.com/YOUR_USERNAME/plant-monitor)
- **Yocto Project:** https://www.yoctoproject.org/
- **meta-raspberrypi:** https://github.com/agherzan/meta-raspberrypi

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Carlos Vargas**
- Automotive Embedded Engineer
- GitHub: [@CarlosVargas91](https://github.com/CarlosVargas91)

---

## 🙏 Acknowledgments

- Yocto Project community
- Raspberry Pi Foundation
- meta-raspberrypi contributors

---

**Built with ❤️ for embedded Linux and plants** 🌱🐧
