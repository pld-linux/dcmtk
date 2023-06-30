# TODO:
# - use system libjpeg? (rather hard: it needs 8/12/16-bit versions; included libijg*
#   are libjpeg 6b with some arithmetic and lossless patches applied;
#   libjpeg 8 already included arithmetic encoding support, but not lossless)
#
# Conditional build:
%bcond_without	icu	# use glibc iconv() instead of icu for charset conversion
# glibc iconv supports only AbortTranscodingOnIllegalSequence conversion flag
# icu supports AbortTranscodingOnIllegalSequence and DiscardIllegalSequences
# standalone libiconv >= 1.8 supports additionally TransliterateIllegalSequences
Summary:	DICOM Toolkit - implementation of DICOM/MEDICOM standard
Summary(pl.UTF-8):	Narzędzia DICOM - implementacja standardu DICOM/MEDICOM
Name:		dcmtk
Version:	3.6.7
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://nero.offis.de/download/dcmtk/release/%{name}-%{version}.tar.gz
# Source0-md5:	e4d519bb315ec3944f3f1d61df465cbd
Patch0:		%{name}-3.6.0-0005-Fixed-includes-for-CharLS-1.0.patch
Patch1:		%{name}-3.6.1-0001-Removed-reference-to-bundled-libcharls.patch
Patch2:		%{name}-3.6.1-0002-Find-and-include-CharLS.patch
Patch3:		%{name}-3.6.1-0003-Create-FindCharLS.cmake.patch
Patch4:		%{name}-3.6.1-0004-Use-cmake-suggested-location-for-CharLS.patch
Patch5:		%{name}-etc.patch
Patch6:		CharLS.patch
Patch7:		%{name}-pc.patch
URL:		https://dcmtk.org/
BuildRequires:	CharLS-devel < 2.0
BuildRequires:	cmake >= 3.0
BuildRequires:	doxygen
%{?with_icu:BuildRequires:	libicu-devel}
BuildRequires:	libpng-devel >= 2:1.2.8
# handled during configuration, but actually not used
#BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel >= 6:4.8.1
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libwrap-devel
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	openjpeg2-devel >= 2
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel >= 1.2.3
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This DICOM ToolKit (DCMTK) package is a set of software libraries and
applications implementing part of the DICOM/MEDICOM Standard.

%description -l pl.UTF-8
Pakiet DICOM ToolKit (DCMTK) to zbiór bibliotek i aplikacji
implementujących część standardu DICOM/MEDICOM.

%package libs
Summary:	DICOM ToolKit shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone DICOM
Group:		Libraries
Requires:	libstdc++ >= 6:4.8.1
Requires:	openssl >= 1.0.1
Requires:	zlib >= 1.2.3

%description libs
DICOM ToolKit shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone DICOM.

%package devel
Summary:	Header files for DCMTK libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek DCMTK
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_icu:Requires:	libicu-devel}
Requires:	libstdc++-devel >= 6:4.8.1
Requires:	libtiff-devel >= 4
Requires:	libwrap-devel
Requires:	openjpeg2-devel >= 2
Requires:	openssl-devel >= 1.0.1
Requires:	zlib-devel >= 1.2.3

%description devel
Header files for DCMTK libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek DCMTK.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# enforce system CharLS
%{__rm} -r dcmjpls/libcharls

%build
install -d build
cd build
# SNDFILE does nothing (as of 3.6.7), just -devel dependency
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DDCMTK_INSTALL_CMKDIR=%{_lib}/cmake/dcmtk \
	-DBUILD_APPS:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DDCMTK_ENABLE_CXX11:BOOL=ON \
	-DDCMTK_USE_CXX11_STL:BOOL=ON \
	-DDCMTK_WITH_CHARLS:BOOL=ON \
	-DDCMTK_WITH_ICONV:BOOL=OFF \
	%{!?with_icu:-DDCMTK_WITH_ICU:BOOL=OFF} \
	-DDCMTK_WITH_OPENSSL:BOOL=ON \
	-DDCMTK_WITH_PNG:BOOL=ON \
	-DDCMTK_WITH_PRIVATE_TAGS:BOOL=ON \
	-DDCMTK_WITH_SNDFILE:BOOL=OFF \
	-DDCMTK_WITH_TIFF:BOOL=ON \
	-DDCMTK_WITH_XML:BOOL=ON \
	-DDCMTK_WITH_ZLIB:BOOL=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_libdir}/cmake/dcmtk/DCMTKTargets.cmake

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE CHANGES COPYRIGHT FAQ HISTORY README
%doc dcmdata/docs/datadict.txt dcmnet/docs/asconfig.txt
%doc dcmqrdb/docs/dcmqr*.txt dcmtls/docs/ciphers.txt
%attr(755,root,root) %{_bindir}/cda2dcm
%attr(755,root,root) %{_bindir}/dcm*
%attr(755,root,root) %{_bindir}/dcod2lum
%attr(755,root,root) %{_bindir}/dconvlum
%attr(755,root,root) %{_bindir}/drtdump
%attr(755,root,root) %{_bindir}/drttest
%attr(755,root,root) %{_bindir}/dsr2html
%attr(755,root,root) %{_bindir}/dsr2xml
%attr(755,root,root) %{_bindir}/dsrdump
%attr(755,root,root) %{_bindir}/dump2dcm
%attr(755,root,root) %{_bindir}/echoscu
%attr(755,root,root) %{_bindir}/findscu
%attr(755,root,root) %{_bindir}/getscu
%attr(755,root,root) %{_bindir}/img2dcm
%attr(755,root,root) %{_bindir}/mkreport
%attr(755,root,root) %{_bindir}/movescu
%attr(755,root,root) %{_bindir}/msgserv
%attr(755,root,root) %{_bindir}/ofstd_tests
%attr(755,root,root) %{_bindir}/pdf2dcm
%attr(755,root,root) %{_bindir}/stl2dcm
%attr(755,root,root) %{_bindir}/storescp
%attr(755,root,root) %{_bindir}/storescu
%attr(755,root,root) %{_bindir}/termscu
%attr(755,root,root) %{_bindir}/wlmscpfs
%attr(755,root,root) %{_bindir}/wltest
%attr(755,root,root) %{_bindir}/xml2dcm
%attr(755,root,root) %{_bindir}/xml2dsr
%dir %{_sysconfdir}/dcmtk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/dcmpstat.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/dcmqrscp.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/filelog.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/logger.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/printers.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/storescp.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/storescu.cfg
%{_datadir}/dcmtk
%{_mandir}/man1/cda2dcm.1*
%{_mandir}/man1/dcm*.1*
%{_mandir}/man1/dcod2lum.1*
%{_mandir}/man1/dconvlum.1*
%{_mandir}/man1/drtdump.1*
%{_mandir}/man1/dsr2html.1*
%{_mandir}/man1/dsr2xml.1*
%{_mandir}/man1/dsrdump.1*
%{_mandir}/man1/dump2dcm.1*
%{_mandir}/man1/echoscu.1*
%{_mandir}/man1/findscu.1*
%{_mandir}/man1/getscu.1*
%{_mandir}/man1/img2dcm.1*
%{_mandir}/man1/movescu.1*
%{_mandir}/man1/pdf2dcm.1*
%{_mandir}/man1/stl2dcm.1*
%{_mandir}/man1/storescp.1*
%{_mandir}/man1/storescu.1*
%{_mandir}/man1/termscu.1*
%{_mandir}/man1/wlmscpfs.1*
%{_mandir}/man1/xml2dcm.1*
%{_mandir}/man1/xml2dsr.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcmr.so.17
%attr(755,root,root) %{_libdir}/libdcmdata.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmdata.so.17
%attr(755,root,root) %{_libdir}/libdcmect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmect.so.17
%attr(755,root,root) %{_libdir}/libdcmdsig.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmdsig.so.17
%attr(755,root,root) %{_libdir}/libdcmfg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmfg.so.17
%attr(755,root,root) %{_libdir}/libdcmimage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmimage.so.17
%attr(755,root,root) %{_libdir}/libdcmimgle.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmimgle.so.17
%attr(755,root,root) %{_libdir}/libdcmiod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmiod.so.17
%attr(755,root,root) %{_libdir}/libdcmjpeg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmjpeg.so.17
%attr(755,root,root) %{_libdir}/libdcmjpls.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmjpls.so.17
%attr(755,root,root) %{_libdir}/libdcmnet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmnet.so.17
%attr(755,root,root) %{_libdir}/libdcmpstat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmpstat.so.17
%attr(755,root,root) %{_libdir}/libdcmqrdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmqrdb.so.17
%attr(755,root,root) %{_libdir}/libdcmrt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmrt.so.17
%attr(755,root,root) %{_libdir}/libdcmseg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmseg.so.17
%attr(755,root,root) %{_libdir}/libdcmpmap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmpmap.so.17
%attr(755,root,root) %{_libdir}/libdcmsr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmsr.so.17
%attr(755,root,root) %{_libdir}/libdcmtract.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmtract.so.17
%attr(755,root,root) %{_libdir}/libdcmtls.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmtls.so.17
%attr(755,root,root) %{_libdir}/libdcmwlm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmwlm.so.17
%attr(755,root,root) %{_libdir}/libi2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libi2d.so.17
%attr(755,root,root) %{_libdir}/libijg12.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libijg12.so.17
%attr(755,root,root) %{_libdir}/libijg16.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libijg16.so.17
%attr(755,root,root) %{_libdir}/libijg8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libijg8.so.17
%attr(755,root,root) %{_libdir}/liboflog.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liboflog.so.17
%attr(755,root,root) %{_libdir}/libofstd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libofstd.so.17

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmr.so
%attr(755,root,root) %{_libdir}/libdcmdata.so
%attr(755,root,root) %{_libdir}/libdcmdsig.so
%attr(755,root,root) %{_libdir}/libdcmect.so
%attr(755,root,root) %{_libdir}/libdcmfg.so
%attr(755,root,root) %{_libdir}/libdcmimage.so
%attr(755,root,root) %{_libdir}/libdcmimgle.so
%attr(755,root,root) %{_libdir}/libdcmiod.so
%attr(755,root,root) %{_libdir}/libdcmjpeg.so
%attr(755,root,root) %{_libdir}/libdcmjpls.so
%attr(755,root,root) %{_libdir}/libdcmnet.so
%attr(755,root,root) %{_libdir}/libdcmpmap.so
%attr(755,root,root) %{_libdir}/libdcmpstat.so
%attr(755,root,root) %{_libdir}/libdcmqrdb.so
%attr(755,root,root) %{_libdir}/libdcmrt.so
%attr(755,root,root) %{_libdir}/libdcmseg.so
%attr(755,root,root) %{_libdir}/libdcmsr.so
%attr(755,root,root) %{_libdir}/libdcmtls.so
%attr(755,root,root) %{_libdir}/libdcmtract.so
%attr(755,root,root) %{_libdir}/libdcmwlm.so
%attr(755,root,root) %{_libdir}/libi2d.so
%attr(755,root,root) %{_libdir}/libijg12.so
%attr(755,root,root) %{_libdir}/libijg16.so
%attr(755,root,root) %{_libdir}/libijg8.so
%attr(755,root,root) %{_libdir}/liboflog.so
%attr(755,root,root) %{_libdir}/libofstd.so
%{_libdir}/cmake/dcmtk
%{_includedir}/dcmtk
%{_pkgconfigdir}/dcmtk.pc
