# keep pkgver AND pkgrel in sync with qt6-qtwayland
# rebuild qt5-qtbase-private-devel consumers on upgrades
pkgname = "qt5-qtbase"
pkgver = "6.10.2"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DBUILD_WITH_PCH=OFF",
    "-DINSTALL_ARCHDATADIR=lib/qt5",
    "-DINSTALL_BINDIR=lib/qt5/bin",
    "-DINSTALL_DATADIR=share/qt5",
    "-DINSTALL_DOCDIR=share/doc/qt5",
    "-DINSTALL_EXAMPLESDIR=lib/qt5/examples",
    "-DINSTALL_INCLUDEDIR=include/qt5",
    "-DINSTALL_MKSPECSDIR=lib/qt5/mkspecs",
    "-DINSTALL_PUBLICBINDIR=usr/bin",
    "-DINSTALL_SYSCONFDIR=/etc/xdg",
    "-DINSTALL_TESTSDIR=lib/qt5/tests",
    "-DQT_BUILD_TESTS=ON",
    "-DQT_FEATURE_journald=OFF",
    "-DQT_FEATURE_libproxy=ON",
    "-DQT_FEATURE_openssl_linked=ON",
    "-DQT_FEATURE_qmake=ON",
    "-DQT_FEATURE_reduce_relocations=OFF",
    "-DQT_FEATURE_syslog=ON",
    "-DQT_FEATURE_system_sqlite=ON",
    "-DQT_FEATURE_vulkan=ON",
    "-DQT_FEATURE_xcb=ON",
    "-DQT_FEATURE_xcb_glx_plugin=ON",
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
pkgdesc = "Qt application framework 6.x"
license = (
    "LGPL-2.1-only AND LGPL-3.0-only AND GPL-3.0-only WITH Qt-GPL-exception-1.0"
)
url = "https://www.qt.io"
source = f"https://download.qt.io/official_releases/qt/{pkgver[:-2]}/{pkgver}/submodules/qtbase-everywhere-src-{pkgver}.tar.xz"
sha256 = "aeb78d29291a2b5fd53cb55950f8f5065b4978c25fb1d77f627d695ab9adf21e"
tool_flags = {"LDFLAGS": ["-Wl,-z,stack-size=0x200000"]}
# FIXME
hardening = ["!int"]
# TODO
options = ["!cross"]

if self.profile().cross:
    hostmakedepends += ["qt5-qtbase"]
    configure_args += ["-DQT_FORCE_BUILD_TOOLS=ON"]

if self.profile().arch == "riscv64":
    # https://bugreports.qt.io/browse/QTBUG-98951
    # our riscv64 is currently emulated, so this breaks anything using qmake from building
    # just disable it on the arch for now, as it falls back to fork and works anyway
    configure_args += ["-DQT_FEATURE_forkfd_pidfd=OFF"]


def init_configure(self):
    if self.has_lto():
        self.configure_args += ["-DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON"]


def init_check(self):
    excl_list = [
        "RunCMake.Sbom",  # fails with latest cmake
        "tst_selftests",  # requires valgrind
        "tst_qmake",  # Could not find qmake spec 'linux-clang'.
        "tst_moc",  # tst_Moc::initTestCase() 'fi.exists()' returned FALSE. ()
        "tst_rcc",  # Could not start "/builddir/qt5-base-6.5.1/build/lib/qt5/libexec/rcc": chdir: No such file or directory
        "tst_qstandardpaths",  # using / as runtime directory ? wrong permission then
        "tst_qresourceengine",  # tst_QResourceEngine::lastModified() '!fi.lastModified().isValid()' returned FALSE.
        "tst_qfilesystemwatcher",  # tst_QFileSystemWatcher::addPaths() Compared lists have different sizes.
        "tst_qpluginloader",  # tst_QPluginLoader::loadDebugObj() 'QFile::exists(QFINDTESTDATA("elftest/debugobj.so"))' returned FALSE. ()
        "tst_qlibrary",  # tst_QLibrary::initTestCase() 'QDir::setCurrent(testdatadir)' returned FALSE. (Could not chdir to )
        "tst_qtextstream",  # tst_QTextStream::initTestCase() '!m_rfc3261FilePath.isEmpty()' returned FALSE. ()
        "test_build_simple_widget_app_qmake",  # fatal error: 'QApplication' file not found
        "test_interface",  # requires Qt5WidgetsConfig.cmake (present in build/lib/cmake/Qt5Widgets/Qt5WidgetsConfig.cmake)
        "test_add_big_resource",  # No data signature found
        "mockplugins",  # Unknown platform linux-clang
        "test_plugin_flavor_static",  # test fails to configure
        "test_plugin_flavor_shared",  # flaky
        "test_plugin_class_name_testpluginnamelower",  # clang error
        "test_plugin_class_name_Test0PluginName",  # clang error
        "test_plugin_class_name_TestPluginNameUpper",  # clang error
        "test_plugin_class_name_Test_Plugin_Name",  # clang error
        "test_plugin_class_name__Test_plugin_name",  # clang error
        "test_import_plugins",  # not run: dep of mockplugins
        "test_add_resources_big_resources",  # No data signature found
        "tst_qaddpreroutine",  # Unknown platform linux-clang
        "test_static_resources",  # Unknown platform linux-clang
        "test_generating_cpp_exports",  # Unknown platform linux-clang
        "test_widgets_app_deployment",  # Subprocess aborted
        "tst_qcolorspace",  # tst_QColorSpace::imageConversion64PM(sRGB -> Adobe RGB) Compared values are not the same
        "tst_qdebug",  # tst_QDebug::qDebugQFlags() Compared values are not the same
        "tst_qdialogbuttonbox",  # tst_QDialogButtonBox::standardButtons() Compared values are not the same
        "tst_qopenglwindow",  # execution failed with exit code Segmentation fault.
        "tst_qimagereader",  # execution failed with exit code Segmentation fault.
        "tst_qicoimageformat",  # execution failed with exit code Segmentation fault.
        "tst_qimage",  # execution failed with exit code Segmentation fault.
        "tst_qpainter",  # execution failed with exit code Segmentation fault.
        "tst_qfont",  # tst_QFont::defaultFamily(serif) 'QFontDatabase::hasFamily(familyForHint)' returned FALSE.
        "tst_qfontdatabase",  # tst_QFontDatabase::systemFixedFont() 'fdbSaysFixed' returned FALSE.
        "tst_qfontmetrics",  # tst_QFontMetrics::zeroWidthMetrics() Compared values are not the same
        "tst_qglyphrun",  # tst_QGlyphRun::mixedScripts() Compared values are not the same
        "tst_qrawfont",  # tst_QRawFont::unsupportedWritingSystem(Default hinting preference) 'layoutFont.familyName() != QString::fromLatin1("QtBidiTestFont")' returned FALSE
        "tst_qtextcursor",  # tst_QTextCursor::insertHtml(insert as text in new block at end of heading) Compared values are not the same
        "tst_qtextdocumentlayout",  # tst_QTextDocumentLayout::imageAtRightAlignedTab() Compared doubles are not the same (fuzzy compare)
        "tst_qtextmarkdownimporter",  # tst_QTextMarkdownImporter::lists(styled spans in list items) Compared values are not the same
        "tst_qopenglconfig",  # tst_QOpenGlConfig::testGlConfiguration() 'context.create()' returned FALSE
        "tst_qopengl",  # tst_QOpenGL::sharedResourceCleanup(Using QWindow) 'ctx->create()' returned FALSE
        "tst_qx11info",  # tst_QX11Info::startupId() Compared values are not the same
        "tst_qdnslookup",  # Resolver functions not found (voidlinux: Some glibc specific DNS Lookup)
        "tst_qfiledialog",  # tst_QFiledialog::historyBack() Compared values are not the same
        "tst_qgraphicsproxywidget",  # tst_QGraphicsProxyWidget::focusOutEvent(widget, focus to other widget) Widget should have focus but doesn't
        "tst_qgraphicsview",  # execution failed with exit code Segmentation fault.
        "tst_qapplication",  # tst_QApplication::libraryPaths() '!testDir.isEmpty()' returned FALSE. ()
        "tst_qfontcombobox",  # tst_QFontComboBox::currentFontChanged() Compared values are not the same
        "tst_qlineedit",  # tst_QLineEdit::setInputMask(keys blank=input) To eat blanks or not? Known issue. Task 43172
        "tst_qmenubar",  # tst_QLineEdit::returnPressed_maskvalidator(mask '999', intfix validator(0,999), input '12<cr>') QIntValidator has changed behaviour. Does not accept spaces.
        "tst_qmetaobject",  # tst_QMetaObject::enumDebugStream(verbosity=3) Not all expected messages were received
        "tst_qmetaobject_compat",  # tst_QMetaObject_CompatQArg::enumDebugStream(verbosity=2) Not all expected messages were received
        "tst_qopenglwidget",  # execution failed with exit code Segmentation fault.
        "tst_qcomplextext",  # tst_QComplexText::bidiCursorMovement(data46) 'newX <= x' returned FALSE
        "tst_qsharedmemory",  # tst_QSharedMemory::simpleThreadedProducerConsumer(POSIX:5 consumers, producer is this) 'p.producer.isAttached()' returned FALSE
        "tst_qaccessibility",  # tst_QAccessibility::mdiSubWindowTest() Compared values are not the same
        "test_qt_extract_metatypes",  # fails to find qt5config.cmake in the test
        "test_qt_add_resources_rebuild",  # ditto
        "test_collecting_plugins",  # unknown platform linux-clang
        "test_standalone_test",  # can't find random .cmake file
        "tst_qstorageinfo",  # Test data requested, but no testdata available
        "tst_qfloat16",  # 0.000000_vs_-1300000.000000 qfloat16 vs qint16 comparison failed
        "tst_qnumeric",  # may fail harmlessly on some hardware due to fp shit
        "tst_qdir",  # flaky
        "tst_qsqltablemodel",  # tst_QSqlTableModel::modelInAnotherThread() 't.isFinished()' returned FALSE. ()
        "tst_qtimer_no_glib",  # times out after 300s
        "tst_qtimer",  # flaky, times out after 300s in tst_QTimer::singleShotToFunctors()
        "tst_qmetatype",  # times out after 300s when busy in threadsafety test
        "tst_qfilesystemmodel",
        "tst_qthread",
        "tst_qthreadstorage",
        "tst_seatv4",  # something with animated cursors
        "tst_wl_reconnect",  # XDG_RUNTIME_DIR not set
        "test_qt_add_ui_*",
    ]
    self.make_check_args += ["-E", "(" + "|".join(excl_list) + ")"]
    self.make_check_env["QT_QPA_PLATFORM"] = "offscreen"
    self.make_check_env["QMAKESPEC"] = f"{self.chroot_cwd}/mkspecs/linux-clang"


def post_install(self):
    # remove installed checks files (because of "-DQT_BUILD_TESTS=ON")
    self.uninstall("usr/tests")
    self.uninstall("usr/lib/qt5/tests")
    self.uninstall("usr/lib/qt5/bin/syslocaleapp")
    self.uninstall("usr/lib/qt5/bin/socketprocess")
    self.uninstall("usr/lib/qt5/bin/qfileopeneventexternal")
    self.uninstall("usr/lib/qt5/bin/qcommandlineparser_test_helper")
    self.uninstall("usr/lib/qt5/bin/paster")
    self.uninstall("usr/lib/qt5/bin/modal_helper")
    self.uninstall("usr/lib/qt5/bin/fileWriterProcess")
    self.uninstall("usr/lib/qt5/bin/echo")
    self.uninstall("usr/lib/qt5/bin/desktopsettingsaware_helper")
    self.uninstall("usr/lib/qt5/bin/crashingServer")
    self.uninstall("usr/lib/qt5/bin/copier")
    self.uninstall("usr/lib/qt5/bin/clientserver")
    self.uninstall("usr/lib/qt5/bin/nospace")
    self.uninstall("usr/lib/qt5/bin/one space")
    self.uninstall("usr/lib/qt5/bin/two space s")
    self.uninstall("usr/lib/qt5/bin/write-read-write")
    self.uninstall("usr/lib/qt5/bin/test*", glob=True)
    self.uninstall("usr/lib/qt5/bin/tst*", glob=True)
    self.install_file(self.files_path / "target_qt.conf", "usr/lib/qt5/bin")
    # eliminate hardlinks
    for f in (self.destdir / "usr/lib/qt5/bin").glob("*6"):
        nsname = f.name.removesuffix("6")
        f.with_name(nsname).unlink()
        self.install_link(f"usr/lib/qt5/bin/{nsname}", f.name)

    # link publicbindir utils to usr/bin, like qmake6
    # used outside of cmake
    self.install_dir("usr/bin")
    with open(
        self.cwd / self.make_dir / "user_facing_tool_links.txt", "r"
    ) as f:
        for line in f.readlines():
            a, b = line.split()
            self.install_link(b, a.replace("../../lib", "../lib"))


@subpackage("qt5-qtbase-gui")
def _(self):
    self.depends += ["hicolor-icon-theme"]
    self.subdesc = "GUI"

    return [
        "usr/lib/libQt5Gui.so.*",
        "usr/lib/libQt5XcbQpa.so.*",
        "usr/lib/libQt5EglFSDeviceIntegration.so.*",
        "usr/lib/libQt5EglFsKmsGbmSupport.so.*",
        "usr/lib/libQt5EglFsKmsSupport.so.*",
        "usr/lib/libQt5OpenGL.so.*",
        "usr/lib/qt5/plugins/generic",
        "usr/lib/qt5/plugins/platforms",
        "usr/lib/qt5/plugins/xcbglintegrations",
        "usr/lib/qt5/plugins/imageformats",
        "usr/lib/qt5/plugins/egldeviceintegrations",
        "usr/lib/qt5/plugins/platforminputcontexts",
        "usr/lib/qt5/plugins/platformthemes",
    ]


def _libpkg(name, libname, desc, extra=[]):
    @subpackage(f"qt5-qtbase-{name}")
    def _(self):
        self.subdesc = desc
        return [f"usr/lib/libQt5{libname}.so.*", *extra]


for _sp in [
    ("opengl-widgets", "OpenGLWidgets", "OpenGL widgets"),
    ("dbus", "DBus", "DBus"),
    ("core", "Core", "Core"),
    (
        "printsupport",
        "PrintSupport",
        "Print support",
        ["usr/lib/qt5/plugins/printsupport"],
    ),
    ("concurrent", "Concurrent", "Concurrency"),
    ("widgets", "Widgets", "Widgets"),
    (
        "network",
        "Network",
        "Network",
        [
            "usr/lib/qt5/plugins/networkinformation",
            "usr/lib/qt5/plugins/tls",
        ],
    ),
    (
        "sql",
        "Sql",
        "SQL",
        [
            "usr/lib/qt5/plugins/sqldrivers",
        ],
    ),
    ("test", "Test", "Test"),
    ("xml", "Xml", "XML"),
]:
    _libpkg(*_sp)


@subpackage("qt5-qtbase-devel-static")
def _(self):
    self.depends = []
    self.install_if = []

    return ["usr/lib/*.a"]


@subpackage("qt5-qtbase-private-devel")
def _(self):
    self.subdesc = "private development files"
    self.depends += [self.with_pkgver("qt5-qtbase-devel")]
    return [
        "usr/include/**/private",
        # usr/lib/cmake/*Private excluded due to anything using qt5_add_qml_module()
        # etc failing to configure as a false-positive in most cases, else build fails
        "usr/lib/qt5/metatypes/*private_metatypes.json",
        # without usr/lib/qt5/mkspecs/modules/*_private.pri qmake won't find libatomic
        "usr/lib/qt5/modules/*Private.json",
    ]


@subpackage("qt5-qtbase-devel")
def _(self):
    self.depends += [
        self.parent,
        # from 6.8 there are some internal .a's that are always installed and
        # cmake detection will fail if they're not there, classic
        self.with_pkgver("qt5-qtbase-devel-static"),
        *makedepends,
    ]
    # keep qt5_add_qml_module() working with split -private-devel by satisfying
    # Qt5::QmlPrivate /usr/include/qt5/QtCore/6.*/QtCore etc with empty dirs
    self.options = ["keepempty"]
    return self.default_devel(
        extra=[
            "usr/bin/androiddeployqt5",
            "usr/bin/qmake6",
            # named based on BUILD_TYPE
            "usr/lib/objects-*",
            "usr/lib/qt5/metatypes",
            "usr/lib/qt5/mkspecs",
            "usr/lib/qt5/modules",
            "usr/lib/*.prl",
        ]
    )
