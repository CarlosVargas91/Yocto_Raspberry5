SUMMARY = "smbus2 is a drop-in replacement for smbus-cffi/smbus-python"
HOMEPAGE = "https://github.com/kplindegaard/smbus2"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=2a3eca2de44816126b3c6f33811a9fba"

SRC_URI[sha256sum] = "36f2288a8e1a363cb7a7b2244ec98d880eb5a728a2494ac9c71e9de7bf6a803a"

inherit pypi setuptools3

PYPI_PACKAGE = "smbus2"

RDEPENDS:${PN} += "python3-core"

COMPATIBLE_MACHINE = "raspberrypi5"