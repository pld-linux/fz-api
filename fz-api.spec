Summary:	FZ-API to access the Fotonic cameras
Summary(pl.UTF-8):	FZ-API pozwalające na dostęp do kamer Fotonic
Name:		fz-api
# see fz_api_src/fzapi.cpp /FZAPI_VERSION
Version:	4.1.2
%define	verdate	20130925
Release:	0.%{verdate}.2
License:	LGPL v3+
Group:		Libraries
Source0:	http://www.fotonic.com/assets/documents/files/131002/fz-linux-api_x64_%{verdate}.tar.gz
# Source0-md5:	bd306ca31230cd632ca4060b5c26b98b
# there is also
#Source1:	http://www.fotonic.com/assets/documents/files/fz-linux-api_x86_20130322.tar.gz
## Source1-md5:	05b3be93d3ba1644c53f5cca9f6029f9
# but it's older and both versions could be built from the same sources
Patch0:		%{name}-system-libyuv.patch
URL:		http://www.fotonic.com/content/Products/downloads.aspx
BuildRequires:	libstdc++-devel
#BuildRequires:	libyuv-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FZ-API to access the Fotonic cameras.

%description -l pl.UTF-8
FZ-API pozwalające na dostęp do kamer Fotonic.

%package devel
Summary:	Header files for FZ-API
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FZ-API
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for FZ-API.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FZ-API.

%package static
Summary:	Static FZ-API library
Summary(pl.UTF-8):	Statyczna biblioteka FZ-API
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FZ-API library.

%description static -l pl.UTF-8
Statyczna biblioteka FZ-API.

%package doc
Summary:	FZ-API documentation
Summary(pl.UTF-8):	Dokumentacja do FZ-API
Group:		Documentation

%description doc
FZ-API documentation.

%description doc -l pl.UTF-8
Dokumentacja do FZ-API.

%prep
%setup -q -c
# system libyuv removed Bayer support making it useless here
#%patch0 -p0

%build
%{__make} -C fz-linux-api_x64/fz_api_src \
	CC="%{__cc}" \
	CPP="%{__cxx}" \
	COMPILERFLAGS="%{rpmcflags} -Wall" \
	LDFLAGS="%{rpmldflags}" \
	TARGET_ARCH= \
	TARGET_OS=Linux

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

install fz-linux-api_x64/fz_api_src/libfz_api.so.1.0 $RPM_BUILD_ROOT%{_libdir}
ln -sf libfz_api.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libfz_api.so.1
ln -sf libfz_api.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libfz_api.so
cp -p fz-linux-api_x64/fz_api_src/libfz_api.a $RPM_BUILD_ROOT%{_libdir}
cp -p fz-linux-api_x64/include/*.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfz_api.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libfz_api.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfz_api.so
%{_includedir}/fz_api.h
%{_includedir}/fz_commands.h
%{_includedir}/fz_types.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libfz_api.a

%files doc
%defattr(644,root,root,755)
%doc fz-linux-api_x64/doc/*.pdf
