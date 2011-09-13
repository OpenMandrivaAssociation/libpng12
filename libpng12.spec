%define libname_orig libpng
%define major 3
%define libname	%mklibname png %{major}
%define develname %mklibname png -d %{major}
%define staticname %mklibname png -d -s %{major}

%bcond_without	uclibc

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng12
Version:	1.2.46
Release:	3
Epoch:		2
License:	zlib
Group:		System/Libraries
URL:		http://www.libpng.org/pub/png/libpng.html
Source:		http://prdownloads.sourceforge.net/libpng/libpng-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		libpng-%{version}-apng.patch.gz
Patch1:		libpng-1.2.36-pngconf-setjmp.patch
Patch2:		libpng-1.2.44-CVE-2008-6218.diff
BuildRequires: 	zlib-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG is
a bit-mapped graphics format similar to the GIF format.  PNG was created to
replace the GIF format, since GIF uses a patented data compression
algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package -n	%{libname}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n	%{develname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	zlib-devel
Conflicts:	png-devel >= 2:1.5
Provides:	png-devel = %{EVRD}

%description -n	%{develname}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install the
libpng package.

%package -n	%{staticname}
Summary:	Development static libraries
Group:		Development/C
Requires:	%{develname} = %{EVRD}
Requires:	zlib-devel
Conflicts:	png-static-devel >= 2:1.5
Provides:	png-static-devel = %{EVRD}

%description -n	%{staticname}
Libpng development static libraries.

%package -n	%{libname}-source
Summary:	Source code of %{libname_orig}
Group:		Development/C

%description -n	%{libname}-source
This package contains the source code of %{libname_orig}.

%prep
%setup -q -n libpng-%{version}
%patch0 -p1 -b .apng
%patch1 -p0 -b .pngconf-setjmp
%patch2 -p0 -b .CVE-2008-6218
./autogen.sh

%build
export CONFIGURE_TOP=`pwd`
%if %{with uclibc}
mkdir -p uclibc
cd uclibc
%configure2_5x	CC="%{uclibc_cc}" \
		CFLAGS="%{uclibc_cflags}" \
		--enable-shared=no \
		--enable-static=yes \
		--with-pic
%make
cd ..
%endif

mkdir -p shared
cd shared
CFLAGS="%{optflags} -O3 -funroll-loops" \
%configure2_5x	--with-pic
%make
cd ..

%check
make -C shared check

%install
%makeinstall_std -C shared
%if %{with uclibc}
install -m644 uclibc/.libs/libpng12.a -D %{buildroot}%{uclibc_root}%{_libdir}/libpng12.a
ln -s libpng12.a %{buildroot}%{uclibc_root}%{_libdir}/libpng.a
%endif

install -d %{buildroot}%{_mandir}/man{3,5}
install -m0644 {libpng,libpngpf}.3 %{buildroot}%{_mandir}/man3
install -m0644 png.5 %{buildroot}%{_mandir}/man5/png3.5

install -d %{buildroot}%{_prefix}/src/%{libname_orig}
cp -a *.c *.h %{buildroot}%{_prefix}/src/%{libname_orig}

# remove unpackaged files
rm -rf %{buildroot}{%{_prefix}/man,%{_libdir}/lib*.la}

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/libpng12-config

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/libpng12.so.*

%files -n %{develname}
%doc *.txt example.c README TODO CHANGES
%{_bindir}/libpng-config
%{_bindir}/libpng12-config
%{multiarch_bindir}/libpng12-config
%{_includedir}/*
%{_libdir}/libpng12.so
%{_libdir}/libpng.so
%{_libdir}/pkgconfig/*
%{_mandir}/man?/*

%files -n %{staticname}
%{_libdir}/libpng*.a
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libpng*.a
%endif

%files -n %{libname}-source
%{_prefix}/src/%{libname_orig}


