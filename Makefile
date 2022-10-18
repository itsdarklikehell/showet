#############################################################################
# Makefile for building: showet
# Generated by qmake (3.1) (Qt 5.15.3)
# Project:  showet.pro
# Template: subdirs
# Command: /usr/lib/qt5/bin/qmake -o Makefile showet.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro'
#############################################################################

MAKEFILE      = Makefile

EQ            = =

first: make_first
QMAKE         = /usr/lib/qt5/bin/qmake
DEL_FILE      = rm -f
CHK_DIR_EXISTS= test -d
MKDIR         = mkdir -p
COPY          = cp -f
COPY_FILE     = cp -f
COPY_DIR      = cp -f -R
INSTALL_FILE  = install -m 644 -p
INSTALL_PROGRAM = install -m 755 -p
INSTALL_DIR   = cp -f -R
QINSTALL      = /usr/lib/qt5/bin/qmake -install qinstall
QINSTALL_PROGRAM = /usr/lib/qt5/bin/qmake -install qinstall -exe
DEL_FILE      = rm -f
SYMLINK       = ln -f -s
DEL_DIR       = rmdir
MOVE          = mv -f
TAR           = tar -cf
COMPRESS      = gzip -9f
DISTNAME      = showet1.0.0
DISTDIR = /home/rizzo/showet/.tmp/showet1.0.0
SUBTARGETS    =  \
		sub-showet-gui


sub-showet-gui-qmake_all:  FORCE
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro'
	cd showet-gui/ && $(MAKE) -f Makefile qmake_all
sub-showet-gui: FORCE
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -f Makefile
sub-showet-gui-make_first: FORCE
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -f Makefile 
sub-showet-gui-all: FORCE
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -f Makefile all
sub-showet-gui-clean: FORCE
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -f Makefile clean
sub-showet-gui-distclean: FORCE
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -f Makefile distclean
sub-showet-gui-install_subtargets: FORCE
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -f Makefile install
sub-showet-gui-uninstall_subtargets: FORCE
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -f Makefile uninstall

Makefile: showet.pro /usr/lib/x86_64-linux-gnu/qt5/mkspecs/linux-g++/qmake.conf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/spec_pre.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/unix.conf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/linux.conf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/sanitize.conf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/gcc-base.conf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/gcc-base-unix.conf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/g++-base.conf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/g++-unix.conf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/qconfig.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_accessibility_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_bootstrap_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_concurrent.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_concurrent_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_core.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_core_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_dbus.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_dbus_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_designer.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_devicediscovery_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_edid_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_egl_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_eglfs_kms_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_eglfsdeviceintegration_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_eventdispatcher_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_fb_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_fontdatabase_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_glx_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_gui.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_gui_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_help.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_input_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_kms_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_linuxaccessibility_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_network.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_network_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_opengl_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_openglextensions.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_openglextensions_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_platformcompositor_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_printsupport.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_printsupport_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qml.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qmlmodels.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qmltest.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qmlworkerscript.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_quick.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_quickwidgets.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_service_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_sql.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_sql_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_svg.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_testlib.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_testlib_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_theme_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_uiplugin.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_uitools.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_vulkan_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_widgets.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_widgets_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xcb_qpa_lib_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xkbcommon_support_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xml.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xml_private.pri \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/qt_functions.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/qt_config.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/linux-g++/qmake.conf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/spec_post.prf \
		.qmake.stash \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/exclusive_builds.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/toolchain.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/default_pre.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/resolve_config.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/default_post.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/warn_on.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/qmake_use.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/file_copies.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/testcase_targets.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/exceptions.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/yacc.prf \
		/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/lex.prf \
		showet.pro
	$(QMAKE) -o Makefile showet.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro'
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/spec_pre.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/unix.conf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/linux.conf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/sanitize.conf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/gcc-base.conf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/gcc-base-unix.conf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/g++-base.conf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/g++-unix.conf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/qconfig.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_accessibility_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_bootstrap_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_concurrent.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_concurrent_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_core.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_core_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_dbus.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_dbus_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_designer.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_devicediscovery_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_edid_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_egl_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_eglfs_kms_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_eglfsdeviceintegration_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_eventdispatcher_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_fb_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_fontdatabase_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_glx_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_gui.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_gui_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_help.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_input_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_kms_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_linuxaccessibility_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_network.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_network_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_opengl_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_openglextensions.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_openglextensions_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_platformcompositor_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_printsupport.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_printsupport_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qml.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qmlmodels.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qmltest.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qmlworkerscript.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_quick.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_quickwidgets.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_service_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_sql.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_sql_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_svg.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_testlib.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_testlib_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_theme_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_uiplugin.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_uitools.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_vulkan_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_widgets.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_widgets_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xcb_qpa_lib_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xkbcommon_support_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xml.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xml_private.pri:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/qt_functions.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/qt_config.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/linux-g++/qmake.conf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/spec_post.prf:
.qmake.stash:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/exclusive_builds.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/toolchain.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/default_pre.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/resolve_config.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/default_post.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/warn_on.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/qmake_use.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/file_copies.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/testcase_targets.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/exceptions.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/yacc.prf:
/usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/lex.prf:
showet.pro:
qmake: FORCE
	@$(QMAKE) -o Makefile showet.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro'

qmake_all: sub-showet-gui-qmake_all FORCE

make_first: sub-showet-gui-make_first  FORCE
all: sub-showet-gui-all  FORCE
clean: sub-showet-gui-clean  FORCE
distclean: sub-showet-gui-distclean  FORCE
	-$(DEL_FILE) Makefile
	-$(DEL_FILE) .qmake.stash
install_subtargets: sub-showet-gui-install_subtargets FORCE
uninstall_subtargets: sub-showet-gui-uninstall_subtargets FORCE

sub-showet-gui-check:
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -f Makefile check
check: sub-showet-gui-check

sub-showet-gui-benchmark:
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -f Makefile benchmark
benchmark: sub-showet-gui-benchmark
install_executable: FORCE
	@test -d $(INSTALL_ROOT)/usr/bin || mkdir -p $(INSTALL_ROOT)/usr/bin
	$(QINSTALL_PROGRAM) /home/rizzo/showet/showet $(INSTALL_ROOT)/usr/bin/showet
	-strip $(INSTALL_ROOT)/usr/bin/showet

uninstall_executable: FORCE
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/bin/showet
	-$(DEL_DIR) $(INSTALL_ROOT)/usr/bin/ 


install_pymodules: FORCE
	@test -d $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet || mkdir -p $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet
	$(QINSTALL) /home/rizzo/showet/platform_3do.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_3do.py
	$(QINSTALL) /home/rizzo/showet/platform_Amstrad.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Amstrad.py
	$(QINSTALL) /home/rizzo/showet/platform_Apple.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Apple.py
	$(QINSTALL) /home/rizzo/showet/platform_Arcade.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Arcade.py
	$(QINSTALL) /home/rizzo/showet/platform_Archimedes.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Archimedes.py
	$(QINSTALL) /home/rizzo/showet/platform_Atari.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Atari.py
	$(QINSTALL) /home/rizzo/showet/platform_Bandai.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Bandai.py
	$(QINSTALL) /home/rizzo/showet/platform_Coleco.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Coleco.py
	$(QINSTALL) /home/rizzo/showet/platform_Commodore.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Commodore.py
	$(QINSTALL) /home/rizzo/showet/platform_Dos.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Dos.py
	$(QINSTALL) /home/rizzo/showet/platform_Elektronika.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Elektronika.py
	$(QINSTALL) /home/rizzo/showet/platform_Enterprise.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Enterprise.py
	$(QINSTALL) /home/rizzo/showet/platform_Fairchild.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Fairchild.py
	$(QINSTALL) /home/rizzo/showet/platform_Gamepark.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Gamepark.py
	$(QINSTALL) /home/rizzo/showet/platform_GCE.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_GCE.py
	$(QINSTALL) /home/rizzo/showet/platform_Java.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Java.py
	$(QINSTALL) /home/rizzo/showet/platform_Linux.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Linux.py
	$(QINSTALL) /home/rizzo/showet/platform_Magnavox.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Magnavox.py
	$(QINSTALL) /home/rizzo/showet/platform_Mattel.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Mattel.py
	$(QINSTALL) /home/rizzo/showet/platform_Microsoft.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Microsoft.py
	$(QINSTALL) /home/rizzo/showet/platform_Nec.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Nec.py
	$(QINSTALL) /home/rizzo/showet/platform_Nintendo.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Nintendo.py
	$(QINSTALL) /home/rizzo/showet/platform_Palm.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Palm.py
	$(QINSTALL) /home/rizzo/showet/platform_Phillips.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Phillips.py
	$(QINSTALL) /home/rizzo/showet/platform_Pico8.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Pico8.py
	$(QINSTALL) /home/rizzo/showet/platform_Sega.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Sega.py
	$(QINSTALL) /home/rizzo/showet/platform_Sinclair.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Sinclair.py
	$(QINSTALL) /home/rizzo/showet/platform_Snk.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Snk.py
	$(QINSTALL) /home/rizzo/showet/platform_Sony.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Sony.py
	$(QINSTALL) /home/rizzo/showet/platform_Spectravideo.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Spectravideo.py
	$(QINSTALL) /home/rizzo/showet/platform_Thomson.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Thomson.py
	$(QINSTALL) /home/rizzo/showet/platform_Tic80.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Tic80.py
	$(QINSTALL) /home/rizzo/showet/platform_Wild.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Wild.py
	$(QINSTALL) /home/rizzo/showet/platformcommon.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platformcommon.py
	$(QINSTALL) /home/rizzo/showet/Remote_Control.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/Remote_Control.py
	$(QINSTALL_PROGRAM) /home/rizzo/showet/showet.py $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/showet.py
	-strip $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/showet.py

uninstall_pymodules: FORCE
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/showet.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/Remote_Control.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platformcommon.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Wild.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Tic80.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Thomson.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Spectravideo.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Sony.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Snk.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Sinclair.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Sega.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Pico8.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Phillips.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Palm.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Nintendo.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Nec.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Microsoft.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Mattel.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Magnavox.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Linux.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Java.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_GCE.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Gamepark.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Fairchild.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Enterprise.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Elektronika.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Dos.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Commodore.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Coleco.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Bandai.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Atari.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Archimedes.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Arcade.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Apple.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_Amstrad.py
	-$(DEL_FILE) -r $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/platform_3do.py
	-$(DEL_DIR) $(INSTALL_ROOT)/usr/lib/python3/dist-packages/showet/ 


install:install_subtargets install_executable install_pymodules  FORCE

uninstall: uninstall_executable uninstall_pymodules uninstall_subtargets FORCE

FORCE:

dist: distdir FORCE
	(cd `dirname $(DISTDIR)` && $(TAR) $(DISTNAME).tar $(DISTNAME) && $(COMPRESS) $(DISTNAME).tar) && $(MOVE) `dirname $(DISTDIR)`/$(DISTNAME).tar.gz . && $(DEL_FILE) -r $(DISTDIR)

distdir: sub-showet-gui-distdir FORCE
	@test -d $(DISTDIR) || mkdir -p $(DISTDIR)
	$(COPY_FILE) --parents /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/spec_pre.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/unix.conf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/linux.conf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/sanitize.conf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/gcc-base.conf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/gcc-base-unix.conf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/g++-base.conf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/common/g++-unix.conf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/qconfig.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_accessibility_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_bootstrap_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_concurrent.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_concurrent_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_core.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_core_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_dbus.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_dbus_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_designer.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_devicediscovery_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_edid_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_egl_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_eglfs_kms_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_eglfsdeviceintegration_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_eventdispatcher_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_fb_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_fontdatabase_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_glx_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_gui.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_gui_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_help.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_input_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_kms_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_linuxaccessibility_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_network.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_network_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_opengl_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_openglextensions.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_openglextensions_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_platformcompositor_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_printsupport.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_printsupport_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qml.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qmlmodels.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qmltest.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_qmlworkerscript.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_quick.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_quickwidgets.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_service_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_sql.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_sql_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_svg.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_testlib.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_testlib_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_theme_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_uiplugin.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_uitools.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_vulkan_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_widgets.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_widgets_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xcb_qpa_lib_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xkbcommon_support_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xml.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/modules/qt_lib_xml_private.pri /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/qt_functions.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/qt_config.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/linux-g++/qmake.conf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/spec_post.prf .qmake.stash /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/exclusive_builds.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/toolchain.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/default_pre.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/resolve_config.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/default_post.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/warn_on.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/qmake_use.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/file_copies.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/testcase_targets.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/exceptions.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/yacc.prf /usr/lib/x86_64-linux-gnu/qt5/mkspecs/features/lex.prf showet.pro $(DISTDIR)/

sub-showet-gui-distdir: FORCE
	@test -d showet-gui/ || mkdir -p showet-gui/
	cd showet-gui/ && ( test -e Makefile || $(QMAKE) -o Makefile /home/rizzo/showet/showet-gui/showet-gui.pro 'QMAKE_CC = cc' 'QMAKE_CXX = g++' 'QMAKE_CFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_CXXFLAGS_RELEASE = -Wdate-time -D_FORTIFY_SOURCE=2 -g -O2 -ffile-prefix-map=/home/rizzo/showet=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security' 'QMAKE_LFLAGS_RELEASE = -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro' ) && $(MAKE) -e -f Makefile distdir DISTDIR=$(DISTDIR)/showet-gui

