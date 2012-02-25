# TODO:
# - use system libjpeg? (8/12/16-bit versions)
#
Summary:	DICOM Toolkit - implementation of DICOM/MEDICOM standard
Summary(pl.UTF-8):	Narzędzia DICOM - implementacja standardu DICOM/MEDICOM
Name:		dcmtk
Version:	3.6.0
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk360/%{name}-%{version}.tar.gz
# Source0-md5:	19409e039e29a330893caea98715390e
Patch0:		%{name}-configure.patch
Patch1:		%{name}-0001-Added-soname-information-for-all-targets.patch
Patch2:		%{name}-0002-Install-libs-in-the-correct-arch-dir.patch
Patch3:		%{name}-0003-Removed-bundled-libcharl-reference-in-dcmjpls.patch
Patch4:		%{name}-0004-Use-system-charls.patch
Patch5:		%{name}-0005-Fixed-includes-for-CharLS-1.0.patch
Patch6:		%{name}-0006-Added-optional-support-for-building-shared-libraries.patch
Patch7:		%{name}-0007-Add-soname-generation-for-modules-which-are-not-in-D.patch
Patch8:		%{name}-link.patch
Patch9:		%{name}-libi2d.patch
Patch10:	%{name}-etc.patch
URL:		http://dicom.offis.de/dcmtk
BuildRequires:	CharLS-devel
BuildRequires:	cmake >= 2.4
BuildRequires:	libpng-devel >= 2:1.2.8
BuildRequires:	libstdc++-devel
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

%description libs
DICOM ToolKit shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone DICOM.

%package devel
Summary:	Header files for DCMTK libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek DCMTK
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel

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
%patch8 -p1
%patch9 -p1
%patch10 -p1

# enforce system CharLS
%{__rm} -r dcmjpls/libcharls

%build
%cmake . \
	-DDCMTK_WITH_OPENSSL=ON \
	-DDCMTK_WITH_PNG=ON \
	-DDCMTK_WITH_PRIVATE_TAGS=ON \
	-DDCMTK_WITH_TIFF=ON \
	-DDCMTK_WITH_XML=ON \
	-DDCMTK_WITH_CHARLS=ON \
	-DDCMTK_WITH_ZLIB=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/dcmtk

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE.360 CHANGES.360 COPYRIGHT FAQ HISTORY README dcmdata/docs/datadict.txt dcmnet/docs/asconfig.txt dcmqrdb/docs/dcmqr*.txt dcmtls/docs/ciphers.txt dcmwlm/docs/wwwapp.txt
%attr(755,root,root) %{_bindir}/dcm*
%attr(755,root,root) %{_bindir}/dcod2lum
%attr(755,root,root) %{_bindir}/dconvlum
%attr(755,root,root) %{_bindir}/dsr2html
%attr(755,root,root) %{_bindir}/dsr2xml
%attr(755,root,root) %{_bindir}/dsrdump
%attr(755,root,root) %{_bindir}/dump2dcm
%attr(755,root,root) %{_bindir}/echoscu
%attr(755,root,root) %{_bindir}/findscu
%attr(755,root,root) %{_bindir}/img2dcm
%attr(755,root,root) %{_bindir}/movescu
%attr(755,root,root) %{_bindir}/pdf2dcm
%attr(755,root,root) %{_bindir}/storescp
%attr(755,root,root) %{_bindir}/storescu
%attr(755,root,root) %{_bindir}/termscu
%attr(755,root,root) %{_bindir}/wlmscpfs
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
%{_mandir}/man1/dsr2html.1*
%{_mandir}/man1/dsr2xml.1*
%{_mandir}/man1/dsrdump.1*
%{_mandir}/man1/dump2dcm.1*
%{_mandir}/man1/echoscu.1*
%{_mandir}/man1/findscu.1*
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
%attr(755,root,root) %{_libdir}/libdcmdata.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmdata.so.3.6
%attr(755,root,root) %{_libdir}/libdcmdsig.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmdsig.so.3.6
%attr(755,root,root) %{_libdir}/libdcmimage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmimage.so.3.6
%attr(755,root,root) %{_libdir}/libdcmimgle.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmimgle.so.3.6
%attr(755,root,root) %{_libdir}/libdcmjpeg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmjpeg.so.3.6
%attr(755,root,root) %{_libdir}/libdcmjpls.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmjpls.so.3.6
%attr(755,root,root) %{_libdir}/libdcmnet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmnet.so.3.6
%attr(755,root,root) %{_libdir}/libdcmpstat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmpstat.so.3.6
%attr(755,root,root) %{_libdir}/libdcmqrdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmqrdb.so.3.6
%attr(755,root,root) %{_libdir}/libdcmsr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmsr.so.3.6
%attr(755,root,root) %{_libdir}/libdcmtls.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmtls.so.3.6
%attr(755,root,root) %{_libdir}/libdcmwlm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcmwlm.so.3.6
%attr(755,root,root) %{_libdir}/libi2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libi2d.so.3.6
%attr(755,root,root) %{_libdir}/libijg12.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libijg12.so.3.6
%attr(755,root,root) %{_libdir}/libijg16.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libijg16.so.3.6
%attr(755,root,root) %{_libdir}/libijg8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libijg8.so.3.6
%attr(755,root,root) %{_libdir}/liboflog.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liboflog.so.3.6
%attr(755,root,root) %{_libdir}/libofstd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libofstd.so.3.6

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdcmdata.so
%attr(755,root,root) %{_libdir}/libdcmdsig.so
%attr(755,root,root) %{_libdir}/libdcmimage.so
%attr(755,root,root) %{_libdir}/libdcmimgle.so
%attr(755,root,root) %{_libdir}/libdcmjpeg.so
%attr(755,root,root) %{_libdir}/libdcmjpls.so
%attr(755,root,root) %{_libdir}/libdcmnet.so
%attr(755,root,root) %{_libdir}/libdcmpstat.so
%attr(755,root,root) %{_libdir}/libdcmqrdb.so
%attr(755,root,root) %{_libdir}/libdcmsr.so
%attr(755,root,root) %{_libdir}/libdcmtls.so
%attr(755,root,root) %{_libdir}/libdcmwlm.so
%attr(755,root,root) %{_libdir}/libi2d.so
%attr(755,root,root) %{_libdir}/libijg12.so
%attr(755,root,root) %{_libdir}/libijg16.so
%attr(755,root,root) %{_libdir}/libijg8.so
%attr(755,root,root) %{_libdir}/liboflog.so
%attr(755,root,root) %{_libdir}/libofstd.so
%{_includedir}/dcmtk
