SUMMARY = "HomeAI custom device tree overlay"
DESCRIPTION = "Enables I2C1, SPI0 for meta-homeai peripherals"
AUTHOR = "Carlos Vargas"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

# This single line tells BitBake:
# - Compile .dts → .dtbo using device tree compiler (dtc)
# - Install .dtbo to /boot/overlays/ automatically
# - No need to write do_compile or do_install!
# Like inherit cmake - framework handles the details
inherit devicetree

# Source DTS file
SRC_URI = "file://homeai-overlay.dts"

# Compatible machines
COMPATIBLE_MACHINE = "raspberrypi5"

# Install to correct location for Raspberry Pi bootloader
do_install:append() {
    install -d ${D}/boot/overlays
    install -m 0644 ${B}/homeai-overlay.dtbo ${D}/boot/overlays/
}

# Ship ALL installed locations in package
FILES:${PN} = " \
    /boot/overlays/homeai-overlay.dtbo \
    /boot/devicetree/homeai-overlay.dtbo \
"