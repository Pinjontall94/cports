pkgname = "qt5-qtbase"
pkgver = "5.15.18_git20251101"
pkgrel = 0
build_style = "configure"
configure_args = [
    "-confirm-license",
    ""
]
hostmakedepends = [
    "cmake",
    "ninja",
    "perl",
    "pkgconf",
]
makedepends = [
    "brotli-devel",
    "cups-devel",
    "dbus-devel",
    "double-conversion-devel",
    "glib-devel",
    "gtk+3-devel",
    "harfbuzz-devel",
    "heimdal-devel",
    "icu-devel",
    "libb2-devel",
    "libinput-devel",
    "libpng-devel",
    "libproxy-devel",
    "libxcb-devel",
    "libxkbcommon-devel",
    "linux-headers",
    "mesa-devel",
    "mtdev-devel",
    "pcre2-devel",
    "sqlite-devel",
    "tslib-devel",
    "vulkan-headers",
    "vulkan-loader-devel",
    "wayland-devel",
    "xcb-util-cursor-devel",
    "xcb-util-devel",
    "xcb-util-image-devel",
    "xcb-util-keysyms-devel",
    "xcb-util-renderutil-devel",
    "xcb-util-wm-devel",
    "zlib-ng-compat-devel",
    "zstd-devel",
]
depends = ["shared-mime-info"]
pkgdesc = "Qt application framework 5.x"
license = (
    "LGPL-2.1-only AND LGPL-3.0-only AND GPL-3.0-only AND Qt-GPL-exception-1.0"
)
url = "https://www.qt.io"
source = f"https://download.qt.io/official_releases/qt/{pkgver[:-2]}/{pkgver}/submodules/qtbase-everywhere-src-{pkgver}.tar.xz"
sha256 = "aeb78d29291a2b5fd53cb55950f8f5065b4978c25fb1d77f627d695ab9adf21e"
tool_flags = {"LDFLAGS": ["-Wl,-z,stack-size=0x200000"]}
# FIXME
hardening = ["!int"]
# TODO
options = ["!cross"]
