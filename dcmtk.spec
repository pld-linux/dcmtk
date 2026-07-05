# TODO:
# - libsndfile support? (-DDCMTK_WITH_SNDFILE=ON)
# - use system libjpeg? (rather hard: it needs 8/12/16-bit versions; included libijg*
#   are libjpeg 6b with some arithmetic and lossless patches applied;
#   libjpeg 8 already included arithmetic encoding support, but not lossless)
#
Summary:	DICOM Toolkit - implementation of DICOM/MEDICOM standard
Summary(pl.UTF-8):	Narzędzia DICOM - implementacja standardu DICOM/MEDICOM
Name:		dcmtk
Version:	3.7.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://dicom.offis.de/download/dcmtk/release/%{name}-%{version}.tar.gz
# Source0-md5:	15531c6d20e188aa8b0f237a84b95bc2
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
BuildRequires:	cmake >= 3.7
BuildRequires:	doxygen
BuildRequires:	libpng-devel >= 2:1.2.8
# handled during configuration, but actually not used
#BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel >= 6:4.8.1
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libwrap-devel
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	openjpeg2-devel >= 2.3.0
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
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
Requires:	openssl >= 1.1.1
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
Requires:	libpng-devel >= 2:1.2.8
Requires:	libstdc++-devel >= 6:4.8.1
Requires:	libtiff-devel >= 4
Requires:	libwrap-devel
Requires:	openjpeg2-devel >= 2.3.0
Requires:	openssl-devel >= 1.1.1
Requires:	zlib-devel >= 1.2.3

%description devel
Header files for DCMTK libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek DCMTK.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1

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
	-DDCMTK_WITH_CHARLS:BOOL=ON \
	-DDCMTK_WITH_ICONV:BOOL=OFF \
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
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE CHANGES COPYRIGHT FAQ HISTORY README
%doc dcmdata/docs/datadict.txt dcmnet/docs/asconfig.txt dcmqrdb/docs/dcmqr*.txt dcmtls/docs/ciphers.txt
%attr(755,root,root) %{_bindir}/cda2dcm
%attr(755,root,root) %{_bindir}/dcm*
%attr(755,root,root) %{_bindir}/dcod2lum
%attr(755,root,root) %{_bindir}/dconvlum
%attr(755,root,root) %{_bindir}/drtdump
%attr(755,root,root) %{_bindir}/dsr2html
%attr(755,root,root) %{_bindir}/dsr2xml
%attr(755,root,root) %{_bindir}/dsrdump
%attr(755,root,root) %{_bindir}/dump2dcm
%attr(755,root,root) %{_bindir}/echoscu
%attr(755,root,root) %{_bindir}/findscu
%attr(755,root,root) %{_bindir}/getscu
%attr(755,root,root) %{_bindir}/img2dcm
%attr(755,root,root) %{_bindir}/json2dcm
%attr(755,root,root) %{_bindir}/mkcsmapper
%attr(755,root,root) %{_bindir}/mkesdb
%attr(755,root,root) %{_bindir}/movescu
%attr(755,root,root) %{_bindir}/pdf2dcm
%attr(755,root,root) %{_bindir}/stl2dcm
%attr(755,root,root) %{_bindir}/storescp
%attr(755,root,root) %{_bindir}/storescu
%attr(755,root,root) %{_bindir}/termscu
%attr(755,root,root) %{_bindir}/wlmscpfs
%attr(755,root,root) %{_bindir}/xml2dcm
%attr(755,root,root) %{_bindir}/xml2dsr
%dir %{_sysconfdir}/dcmtk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/consolog.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/dcmpstat.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/dcmqrprf.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/dcmqrscp.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/filelog.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/logger.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/printers.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/storescp.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dcmtk/storescu.cfg
%{_datadir}/dcmtk-%{version}
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
%{_mandir}/man1/json2dcm.1*
%{_mandir}/man1/mkcsmapper.1*
%{_mandir}/man1/mkesdb.1*
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
%{_libdir}/libcmr.so.*.*.*
%ghost %{_libdir}/libcmr.so.20
%{_libdir}/libdcmdata.so.*.*.*
%ghost %{_libdir}/libdcmdata.so.20
%{_libdir}/libdcmect.so.*.*.*
%ghost %{_libdir}/libdcmect.so.20
%{_libdir}/libdcmdsig.so.*.*.*
%ghost %{_libdir}/libdcmdsig.so.20
%{_libdir}/libdcmfg.so.*.*.*
%ghost %{_libdir}/libdcmfg.so.20
%{_libdir}/libdcmimage.so.*.*.*
%ghost %{_libdir}/libdcmimage.so.20
%{_libdir}/libdcmimgle.so.*.*.*
%ghost %{_libdir}/libdcmimgle.so.20
%{_libdir}/libdcmiod.so.*.*.*
%ghost %{_libdir}/libdcmiod.so.20
%{_libdir}/libdcmjpeg.so.*.*.*
%ghost %{_libdir}/libdcmjpeg.so.20
%{_libdir}/libdcmjpls.so.*.*.*
%ghost %{_libdir}/libdcmjpls.so.20
%{_libdir}/libdcmnet.so.*.*.*
%ghost %{_libdir}/libdcmnet.so.20
%{_libdir}/libdcmpstat.so.*.*.*
%ghost %{_libdir}/libdcmpstat.so.20
%{_libdir}/libdcmqrdb.so.*.*.*
%ghost %{_libdir}/libdcmqrdb.so.20
%{_libdir}/libdcmrt.so.*.*.*
%ghost %{_libdir}/libdcmrt.so.20
%{_libdir}/libdcmseg.so.*.*.*
%ghost %{_libdir}/libdcmseg.so.20
%{_libdir}/libdcmpmap.so.*.*.*
%ghost %{_libdir}/libdcmpmap.so.20
%{_libdir}/libdcmsr.so.*.*.*
%ghost %{_libdir}/libdcmsr.so.20
%{_libdir}/libdcmtract.so.*.*.*
%ghost %{_libdir}/libdcmtract.so.20
%{_libdir}/libdcmtls.so.*.*.*
%ghost %{_libdir}/libdcmtls.so.20
%{_libdir}/libdcmwlm.so.*.*.*
%ghost %{_libdir}/libdcmwlm.so.20
%{_libdir}/libdcmxml.so.*.*.*
%ghost %{_libdir}/libdcmxml.so.20
%{_libdir}/libi2d.so.*.*.*
%ghost %{_libdir}/libi2d.so.20
%{_libdir}/libijg12.so.*.*.*
%ghost %{_libdir}/libijg12.so.20
%{_libdir}/libijg16.so.*.*.*
%ghost %{_libdir}/libijg16.so.20
%{_libdir}/libijg8.so.*.*.*
%ghost %{_libdir}/libijg8.so.20
%{_libdir}/liboficonv.so.*.*.*
%ghost %{_libdir}/liboficonv.so.20
%{_libdir}/liboflog.so.*.*.*
%ghost %{_libdir}/liboflog.so.20
%{_libdir}/libofstd.so.*.*.*
%ghost %{_libdir}/libofstd.so.20

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcmr.so
%{_libdir}/libdcmdata.so
%{_libdir}/libdcmdsig.so
%{_libdir}/libdcmect.so
%{_libdir}/libdcmfg.so
%{_libdir}/libdcmimage.so
%{_libdir}/libdcmimgle.so
%{_libdir}/libdcmiod.so
%{_libdir}/libdcmjpeg.so
%{_libdir}/libdcmjpls.so
%{_libdir}/libdcmnet.so
%{_libdir}/libdcmpmap.so
%{_libdir}/libdcmpstat.so
%{_libdir}/libdcmqrdb.so
%{_libdir}/libdcmrt.so
%{_libdir}/libdcmseg.so
%{_libdir}/libdcmsr.so
%{_libdir}/libdcmtls.so
%{_libdir}/libdcmtract.so
%{_libdir}/libdcmwlm.so
%{_libdir}/libdcmxml.so
%{_libdir}/libi2d.so
%{_libdir}/libijg12.so
%{_libdir}/libijg16.so
%{_libdir}/libijg8.so
%{_libdir}/liboficonv.so
%{_libdir}/liboflog.so
%{_libdir}/libofstd.so
%{_libdir}/cmake/dcmtk
%{_includedir}/dcmtk
%{_pkgconfigdir}/dcmtk.pc
