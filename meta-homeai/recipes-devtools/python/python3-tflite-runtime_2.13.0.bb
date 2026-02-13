SUMMARY = "TensorFlow Lite Runtime for Python"
DESCRIPTION = "Lightweight library for deploying TensorFlow Lite models"
HOMEPAGE = "https://www.tensorflow.org/lite"
AUTHOR = "Carlos Vargas"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/Apache-2.0;md5=89aea4e17d99a7cacdbeed46a0096b10"

inherit python3-dir

# Use local file (no download needed)
SRC_URI = "file://tflite_runtime-2.13.0-cp310-cp310-manylinux2014_aarch64.whl"

S = "${WORKDIR}"

# Build-time dependency
DEPENDS += "unzip-native"

# Runtime dependencies
RDEPENDS:${PN} += " \
    python3-numpy \
    python3-core \
"

COMPATIBLE_MACHINE = "raspberrypi5"

do_install() {
    install -d ${D}${PYTHON_SITEPACKAGES_DIR}
    
    # Unzip wheel
    cd ${WORKDIR}
    unzip -q tflite_runtime-*.whl -d ${D}${PYTHON_SITEPACKAGES_DIR}
}

FILES:${PN} += "${PYTHON_SITEPACKAGES_DIR}/*"