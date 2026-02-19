SUMMARY = "Python bindings for Linux SPI access through spidev"
HOMEPAGE = "https://github.com/doceme/py-spidev"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=2077511c543a7c85245a516c47f4de78"

SRC_URI[sha256sum] = "14dbc37594a4aaef85403ab617985d3c3ef464d62bc9b769ef552db53701115b"

inherit pypi setuptools3

PYPI_PACKAGE = "spidev"

RDEPENDS:${PN} += "python3-core"

COMPATIBLE_MACHINE = "raspberrypi5"