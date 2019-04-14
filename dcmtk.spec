# TODO:
# - use system libjpeg? (rather hard: it needs 8/12/16-bit versions; included libijg*
#   are libjpeg 6b with some arithmetic and lossless patches applied;
#   libjpeg 8 already inclded arithmetic encoding support, but not lossless)
#
Summary:	DICOM To:olkit - implementation of DICOM/MEDICOM standard
Summary(pl.UTF-8):	Narzędzia DICOM - implementacja standardu DICOM/MEDICOM
Name:		dcmtk
Version:	3.6.3
Release:	2
License:	BSD
Group:		Libraries
Source0:	ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk363/%{name}-%{version}.tar.gz
# Source0-md5:	2f79082d52cbbb06a360f48b4a9c61be
Patch0:		%{name}-3.6.0-0005-Fixed-includes-for-CharLS-1.0.patch
Patch1:		%{name}-3.6.1-0001-Removed-reference-to-bundled-libcharls.patch
Patch2:		%{name}-3.6.1-0002-Find-and-include-CharLS.patch
Patch3:		%{name}-3.6.1-0003-Create-FindCharLS.cmake.patch
Patch4:		%{name}-3.6.1-0004-Use-cmake-suggested-location-for-CharLS.patch
Patch5:		%{name}-etc.patch
Patch6:		CharLS.patch
URL:		http://dicom.offis.de/dcmtk
BuildRequires:	CharLS-devel < 2.0
BuildRequires:	cmake >= 2.4
BuildRequires:	libpng-devel >= 2:1.2.8
BuildRequires:	libstdc++-devel >= 6:4.8.1
BuildRequires:	libtiff-devel >= 3.7.0
BuildRequires:	libwrap-devel
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	openssl-devel >= 0.9.8
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

%description libs
DICOM ToolKit shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone DICOM.

%package devel
Summary:	Header files for DCMTK libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek DCMTK
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.8.1

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

# enforce system CharLS
%{__rm} -r dcmjpls/libcharls

%build
%cmake . \
	-DDCMTK_INSTALL_ETCDIR=%{_sysconfdir}/%{name} \
	-DDCMTK_INSTALL_LIBDIR=%{_lib} \
	-DDCMTK_INSTALL_CMKDIR=%{_lib}/cmake/dcmtk \
	-DBUILD_APPS:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DDCMTK_USE_CXX11_STL:BOOL=ON \
	-DDCMTK_WITH_OPENSSL:BOOL=ON \
	-DDCMTK_WITH_PNG:BOOL=ON \
	-DDCMTK_WITH_PRIVATE_TAGS:BOOL=ON \
	-DDCMTK_WITH_TIFF:BOOL=ON \
	-DDCMTK_WITH_XML:BOOL=ON \
	-DDCMTK_WITH_CHARLS=ON \
	-DDCMTK_WITH_ZLIB:BOOL=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%{_mandir}/man1/storescp.1*
%{_mandir}/man1/storescu.1*
%{_mandir}/man1/termscu.1*
%{_mandir}/man1/wlmscpfs.1*
%{_mandir}/man1/xml2dcm.1*
%{_mandir}/man1/xml2dsr.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcmr.so.13
%attr(755,root,root) %{_libdir}/libdcmdata.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmdata.so.13
%attr(755,root,root) %{_libdir}/libdcmdsig.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmdsig.so.13
%attr(755,root,root) %{_libdir}/libdcmfg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmfg.so.13
%attr(755,root,root) %{_libdir}/libdcmimage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmimage.so.13
%attr(755,root,root) %{_libdir}/libdcmimgle.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmimgle.so.13
%attr(755,root,root) %{_libdir}/libdcmiod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmiod.so.13
%attr(755,root,root) %{_libdir}/libdcmjpeg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmjpeg.so.13
%attr(755,root,root) %{_libdir}/libdcmjpls.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmjpls.so.13
%attr(755,root,root) %{_libdir}/libdcmnet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmnet.so.13
%attr(755,root,root) %{_libdir}/libdcmpstat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmpstat.so.13
%attr(755,root,root) %{_libdir}/libdcmqrdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmqrdb.so.13
%attr(755,root,root) %{_libdir}/libdcmrt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmrt.so.13
%attr(755,root,root) %{_libdir}/libdcmseg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmseg.so.13
%attr(755,root,root) %{_libdir}/libdcmpmap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmpmap.so.13
%attr(755,root,root) %{_libdir}/libdcmsr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmsr.so.13
%attr(755,root,root) %{_libdir}/libdcmtract.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmtract.so.13
%attr(755,root,root) %{_libdir}/libdcmtls.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmtls.so.13
%attr(755,root,root) %{_libdir}/libdcmwlm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmwlm.so.13
%attr(755,root,root) %{_libdir}/libi2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libi2d.so.13
%attr(755,root,root) %{_libdir}/libijg12.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libijg12.so.13
%attr(755,root,root) %{_libdir}/libijg16.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libijg16.so.13
%attr(755,root,root) %{_libdir}/libijg8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libijg8.so.13
%attr(755,root,root) %{_libdir}/liboflog.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liboflog.so.13
%attr(755,root,root) %{_libdir}/libofstd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libofstd.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmr.so
%attr(755,root,root) %{_libdir}/libdcmdata.so
%attr(755,root,root) %{_libdir}/libdcmdsig.so
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
