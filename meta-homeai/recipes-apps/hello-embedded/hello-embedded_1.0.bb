SUMMARY = "Hello Embedded - First custom recipe in meta-homeai"
DESCRIPTION = "Simple C application to verify custom layer is working"
AUTHOR = "Carlos Vargas"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://hello-embedded.c"

S = "${WORKDIR}"

do_compile() {
    ${CC} ${CFLAGS} ${LDFLAGS} hello-embedded.c -o hello-embedded
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 hello-embedded ${D}${bindir}/hello-embedded
}