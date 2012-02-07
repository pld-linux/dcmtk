# TODO:
# - shared libs
# - use system libjpeg?
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
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
URL:		http://dicom.offis.de/dcmtk
BuildRequires:	libpng-devel >= 2:1.2.8
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel >= 3.7.0
BuildRequires:	libwrap-devel
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	zlib-devel >= 1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This DICOM ToolKit (DCMTK) package is a set of software libraries and
applications implementing part of the DICOM/MEDICOM Standard.

%description -l pl.UTF-8
Pakiet DICOM ToolKit (DCMTK) to zbiór bibliotek i aplikacji
implementujących część standardu DICOM/MEDICOM.

%package devel
Summary:	Header files for DCMTK libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek DCMTK
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for DCMTK libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek DCMTK.

%package static
Summary:	Static DCMTK libraries
Summary(pl.UTF-8):	Statyczne biblioteki DCMTK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DCMTK libraries.

%description static -l pl.UTF-8
Statyczne biblioteki DCMTK.

%package apidocs
Summary:	DCMTK API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek DCMTK
Group:		Documentation

%description apidocs
API documentation for DCMTK library.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek DCMTK.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--datadir=%{_datadir}/dcmtk \
	--sysconfdir=%{_sysconfdir}/dcmtk

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-all \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE.360 CHANGES.360 COPYRIGHT FAQ HISTORY README
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

%files devel
%defattr(644,root,root,755)
%{_includedir}/dcmtk

#%files static
#%defattr(644,root,root,755)
%{_libdir}/libcharls.a
%{_libdir}/libdcmdata.a
%{_libdir}/libdcmdsig.a
%{_libdir}/libdcmimage.a
%{_libdir}/libdcmimgle.a
%{_libdir}/libdcmjpeg.a
%{_libdir}/libdcmjpls.a
%{_libdir}/libdcmnet.a
%{_libdir}/libdcmpstat.a
%{_libdir}/libdcmqrdb.a
%{_libdir}/libdcmsr.a
%{_libdir}/libdcmtls.a
%{_libdir}/libdcmwlm.a
%{_libdir}/libi2d.a
%{_libdir}/libijg12.a
%{_libdir}/libijg16.a
%{_libdir}/libijg8.a
%{_libdir}/liboflog.a
%{_libdir}/libofstd.a

#%if %{with apidocs}
#%files apidocs
#%defattr(644,root,root,755)
#%doc apidocs/*
#%endif
