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