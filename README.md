```bash
sudo apt update
sudo apt install -y gawk wget git diffstat unzip texinfo gcc build-essential \
  chrpath socat cpio python3 python3-pip python3-pexpect xz-utils \
  debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa \
  libsdl1.2-dev pylint xterm python3-subunit mesa-common-dev zstd \
  liblz4-tool file locales libacl1

sudo locale-gen en_US.UTF-8

# Clone Poky (core Yocto) - takes ~5 min
git clone -b kirkstone git://git.yoctoproject.org/poky.git

# Clone Raspberry Pi BSP
git clone -b kirkstone https://github.com/agherzan/meta-raspberrypi.git

# Clone OpenEmbedded layers
git clone -b kirkstone https://github.com/openembedded/meta-openembedded.git

cd ~/yocto-ai-project
source poky/oe-init-build-env build-rpi5

nano conf/local.conf
```

# Find disk number
diskutil list

# Unmount (don't eject)
diskutil unmountDisk /dev/disk4

# Flash directly - this erases everything
sudo dd if=~/Downloads/rpi5-image.wic of=/dev/rdisk4 bs=4m status=progress

# Sync and eject
sync
diskutil eject /dev/disk4

**Make these changes:**

1. **Find this line (around line 34):**

   MACHINE ??= "qemux86-64"

   **Change to:**

   MACHINE ?= "raspberrypi5"

# Enable systemd
   DISTRO_FEATURES:append = " systemd"
   VIRTUAL-RUNTIME_init_manager = "systemd"
   DISTRO_FEATURES_BACKFILL_CONSIDERED = "sysvinit"
   VIRTUAL-RUNTIME_initscripts = ""
   
   # Enable UART for serial console
   ENABLE_UART = "1"
   
   # Optimize for 9 cores
   BB_NUMBER_THREADS = "9"
   PARALLEL_MAKE = "-j 9"
   
   # Add useful tools
   IMAGE_INSTALL:append = " python3 python3-pip nano htop i2c-tools"

```bash
nano conf/bblayers.conf

BBLAYERS ?= " \
  /home/goyii/yocto-ai-project/poky/meta \
  /home/goyii/yocto-ai-project/poky/meta-poky \
  /home/goyii/yocto-ai-project/poky/meta-yocto-bsp \
  /home/goyii/yocto-ai-project/meta-raspberrypi \
  /home/goyii/yocto-ai-project/meta-openembedded/meta-oe \
  /home/goyii/yocto-ai-project/meta-openembedded/meta-python \
  /home/goyii/yocto-ai-project/meta-openembedded/meta-networking \
  "

bitbake-layers show-layers
```

**Build an image**
```bash
bitbake core-image-base
```

**Decompress**
```bash
# In Ubuntu VM - decompress new image
cd ~/Documents/Yocto/yocto-ai-project/build-rpi5/tmp/deploy/images/raspberrypi5/

bzcat core-image-base-raspberrypi5.wic.bz2 > rpi5-image-v2.wic

ip addr show | grep "inet "
```

**Create a recipe**
# Step 1: Create directory structure
mkdir -p ~/Documents/Yocto/yocto-ai-project/meta-homeai/recipes-apps/hello-embedded/files

# Step 2: Create C source file
cat > ~/Documents/Yocto/yocto-ai-project/meta-homeai/recipes-apps/hello-embedded/files/hello-embedded.c << 'EOF'


CMakeLists.txt:              hello-embedded_1.0.bb:
────────────────             ──────────────────────────
✅ Find sources              ✅ Find sources (SRC_URI)
✅ Compile                   ✅ Compile (do_compile)
✅ Link                      ✅ Link
❌ Download sources          ✅ Download from internet (git/http)
❌ License checking          ✅ Verify license (LIC_FILES_CHKSUM)
❌ Cross-compile setup       ✅ Cross-compile automatically
❌ Package creation          ✅ Create .ipk/.deb/.rpm package
❌ Dependency management     ✅ Handle all dependencies
❌ Install to rootfs         ✅ Install to target rootfs (do_install)
❌ Shared state cache        ✅ Cache results (sstate)

Tool              Purpose
────────────────────────────────────────────────────
pyenv             Python version isolation
virtualenv        Python package isolation
source oe-init    BitBake environment isolation
Docker            Full OS isolation

## Complete Picture
```
STEP 1: .dts file
"Describes the hardware configuration"
(your homeai-overlay.dts)
        ↓ compiled by dtc

STEP 2: .dtbo file
"Binary overlay sitting in /boot/overlays/"
(homeai-overlay.dtbo)
= File EXISTS but NOT yet active
        ↓ activated by

STEP 3: config.txt
"Bootloader reads this and LOADS the overlay"
dtoverlay=homeai-overlay
= NOW the overlay is active!
= Linux kernel sees I2C, SPI enabled
        ↓ tells kernel

STEP 4: Linux kernel
"Reads combined device tree"
= Loads i2c-bcm2835 driver
= Loads spi-bcm2835 driver
= /dev/i2c-1 appears!
= /dev/spidev0.0 appears!
```

**Flashing SD**
diskutil list
diskutil unmountDisk /dev/disk4
sudo dd if=/Users/goyi/Downloads/rpi5-image-v6-tflite.wic of=/dev/rdisk4 bs=4m status=progress
sync
diskutil eject /dev/disk4

**Connect to raspberry pi5**
ssh-keygen -R <IPADDRESS>
ssh root@<IPADDRESS>