# Not working yet because no internet connection
SUMMARY = "Python Imaging Library (Fork)"
HOMEPAGE = "https://python-pillow.org"
LICENSE = "HPND"
LIC_FILES_CHKSUM = "file://LICENSE;md5=ad160c36d9105d5d0a8e800e03dd73c5"

SRC_URI[sha256sum] = "9c82b5b3e043c7af0d1e5c97a76e51b5f516e34ad9e1e1ff96f66a9cb96e973f"

inherit pypi setuptools3

PYPI_PACKAGE = "pillow"

DEPENDS += "zlib jpeg freetype"

RDEPENDS:${PN} += " \
    python3-core \
    python3-math \
"

COMPATIBLE_MACHINE = "raspberrypi5"