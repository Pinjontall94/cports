pkgname = "libobjc2"
pkgver = "2.3"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DTESTS=on",
    "-DCMAKE_BUILD_TYPE=Release",
    "-DGNUSTEP_INSTALL_TYPE=NONE",
    "-DEMBEDDED_BLOCKS_RUNTIME=ON",
    "-DOLDABI_COMPAT=OFF",
]
hostmakedepends = [
    "clang-tools-extra",
    "cmake",
    "gettext",
    "ninja",
    "pkgconf",
]
pkgdesc = "Objective-C runtime library intended for use with Clang"
license = "MIT"
url = "https://www.gnustep.org"
source = f"https://github.com/gnustep/libobjc2/archive/v{pkgver}.tar.gz"
sha256 = "5ead2276b42a534ac40437ce53b2231320b985539dc325453d93874be8d92869"
