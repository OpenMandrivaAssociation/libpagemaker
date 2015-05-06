%global major 0.0
%define libname %mklibname pagemaker %major
%define devname %mklibname -d pagemaker
%global apiversion 0.0

Name: libpagemaker
Version: 0.0.2
Release: 0.1
Group:	System/Libraries
Summary: A library for import of Adobe PageMaker documents

License: MPLv2.0
URL: http://wiki.documentfoundation.org/DLP/Libraries/libpagemaker
Source: http://dev-www.libreoffice.org/src/%{name}/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: help2man
BuildRequires: pkgconfig(librevenge-0.0)

%description
libpagemaker is library providing ability to interpret and import
Adobe PageMaker documents into various applications.

%package -n %libname
Summary: A library for import of Adobe PageMaker documents
Group:	System/Libraries

%description -n %libname
libpagemaker is library providing ability to interpret and import
Adobe PageMaker documents into various applications.

%package -n %devname
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{version}-%{release}

%description -n %devname
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: Documentation of %{name} API
BuildArch: noarch

%description doc
The %{name}-doc package contains documentation files for %{name}.

%package tools
Summary: Tools to transform Adobe PageMaker documents into other formats
Requires: %{libname} = %{version}-%{release}

%description tools
Tools to transform Adobe PageMaker documents into other formats.
Currently supported: SVG, raw.

%prep
%setup -q

%build
%configure2_5x --disable-silent-rules --disable-werror
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
%make

export LD_LIBRARY_PATH=`pwd`/src/lib/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
help2man -N -n 'debug the conversion library' -o pmd2raw.1 ./src/conv/raw/.libs/pmd2raw
help2man -N -n 'convert PageMaker document into SVG' -o pmd2svg.1 ./src/conv/svg/.libs/pmd2svg

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 pmd2*.1 %{buildroot}/%{_mandir}/man1


%files -n %libname
%doc AUTHORS COPYING NEWS
%{_libdir}/%{name}-%{apiversion}.so.*

%files -n %devname
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%doc COPYING
%doc docs/doxygen/html

%files tools
%{_bindir}/pmd2raw
%{_bindir}/pmd2svg
%{_mandir}/man1/pmd2raw.1*
%{_mandir}/man1/pmd2svg.1*
