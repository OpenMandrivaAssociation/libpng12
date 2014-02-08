%define oname	libpng
%define api	12
%define major	0
%define libname %mklibname png %{api} %{major}

%define oldmajor 3
%define oldlib %mklibname png %{oldmajor}

Summary:	A library of functions for manipulating PNG image format files
Name:		%{oname}%{api}
Epoch:		2
Version:	1.2.49
Release:	13
License:	zlib
Group:		System/Libraries
Url:		http://www.libpng.org/pub/png/libpng.html
Source0:	http://prdownloads.sourceforge.net/libpng/%{oname}-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		libpng-%{version}-apng.patch.gz
Patch1:		libpng-1.2.36-pngconf-setjmp.patch
Patch2:		libpng-1.2.44-CVE-2008-6218.diff
Patch3:		libpng-1.2.46-fix-libdir-pkgconfig-lib64-conflict.patch
Patch4:		libpng-automake-1.13.patch
BuildRequires:	pkgconfig(zlib)

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
Obsoletes:	%{_lib}png12 < 2:1.2.49-8
Conflicts:	%{oldlib} < 2:1.2.46-5

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n	%{oldlib}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries

%description -n	%{oldlib}
This package contains the library needed to run programs dynamically
linked with really old versions of libpng.

%prep
%setup -qn %{oname}-%{version}
%apply_patches
autoreconf -ivf

%build
export CONFIGURE_TOP=`pwd`

mkdir -p shared
cd shared
CFLAGS="%{optflags} -O3 -funroll-loops" \
%configure2_5x \
	--with-pic \
	--disable-static
%make
cd ..

%check
make -C shared check

%install
%makeinstall_std -C shared

rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}/*.so
rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{_datadir}

%files -n %{libname}
%{_libdir}/libpng%{api}.so.%{major}*

%files -n %{oldlib}
%{_libdir}/libpng.so.%{oldmajor}*

