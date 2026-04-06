pkgname = "86Box"
pkgver = "5.3"
pkgrel = 1
build_style = "cmake_configure"
configure_args = [
    "-DCMAKE_TOOLCHAIN_FILE=../cmake/flags-gcc-x86_64.cmake"
]
make_dir = "."
hostmakedepends = ["pkgconf", "cmake", "libatomic-chimera", "ninja"]
makedepends = [
    "fluidsynth-devel",
    "freetype-devel",
    "libpng-devel",
    "libslirp-devel",
    "libsndfile-devel",
    "rtmidi-devel",
    "sdl2-compat-devel",
    "openal-soft-devel",
    "qt6-qtbase-devel",
    "qt6-qttools-devel",
    "qt6-qt5compat-devel"
]
pkgdesc = "Emulator of x86-based machines."
license = "GPL-2.0"
url = "https://86box.net"
source = f"$(GITHUB_SITE)/86Box/86box-{pkgver}.tar.gz"
sha256 = "758f45dcb7465d88a7a0ef9e7764ea63fac65830bc1398f5ad03f76bac77934b"
