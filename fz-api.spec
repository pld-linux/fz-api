Summary:	FZ-API to access the Fotonic cameras
Summary(pl.UTF-8):	FZ-API pozwalające na dostęp do kamer Fotonic
Name:		fz-api
# version unknown
Version:	0
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	http://www.fotonic.com/assets/documents/downloads/fz-linux-api_x64.tar.gz.zip
# Source0-md5:	74cc0d1dcd13a6fe98baae01777cb1a3
# tarballs differ only by pre-compiled binaries; we use only sources and docs, which are the same
#Source1:	http://www.fotonic.com/assets/documents/downloads/fz-linux-api_x86.tar.gz.zip
## Source1-md5:	bb37c1bf0bfbd3f06e8f6b0393a46b87
URL:		http://www.fotonic.com/content/Products/downloads.aspx
BuildRequires:	libstdc++-devel
BuildRequires:	libyuv-devel
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

tar xzf fz-linux-api_x64.tar.gz
# not required so far
#tar xzf fz-linux-api_x86.tar.gz

# adjust libyuv include
%{__sed} -i -e 's,libyuv/libyuv\.h,libyuv.h,' fz-linux-api_x64/fz_api_src/fzapi.cpp
# be consistent with docs and precompiled binaries
%{__sed} -i -e 's,libFZ_API,libfz_api,' fz-linux-api_x64/fz_api_src/Makefile

%build
%{__make} -C fz-linux-api_x64/fz_api_src \
	CC="%{__cc}" \
	CPP="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC -Wall" \
	LDFLAGS_D_OUT="%{rpmldflags} -shared -Wl,-soname,libfz_api.so.1 -o libfz_api.so.1.0" \
	LDFLAGS_PLAIN="-lyuv -lpthread" \
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
