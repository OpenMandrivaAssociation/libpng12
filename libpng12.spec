%define libname_orig libpng
%define major 0
%define libname %mklibname png12
# %{major}

%define oldmajor 3
%define oldlib %mklibname png %{oldmajor}

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng12
Version:	1.2.49
Release:	6
Epoch:		2
License:	zlib
Group:		System/Libraries
URL:		http://www.libpng.org/pub/png/libpng.html
Source0:	http://prdownloads.sourceforge.net/libpng/libpng-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		libpng-%{version}-apng.patch.gz
Patch1:		libpng-1.2.36-pngconf-setjmp.patch
Patch2:		libpng-1.2.44-CVE-2008-6218.diff
Patch3:		libpng-1.2.46-fix-libdir-pkgconfig-lib64-conflict.patch
Patch4:		libpng-automake-1.13.patch
BuildRequires:	zlib-devel
BuildRequires:	automake

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
%setup -q -n libpng-%{version}
%patch0 -p1 -b .apng
%patch1 -p0 -b .pngconf-setjmp
%patch2 -p0 -b .CVE-2008-6218
%patch3 -p1 -b .lib64~
%patch4 -p1 -b .automake113~
autoreconf -ivf

%build
export CONFIGURE_TOP=`pwd`

mkdir -p shared
cd shared
CFLAGS="%{optflags} -O3 -funroll-loops" \
%configure2_5x	--with-pic --disable-static
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
%{_libdir}/libpng12.so.%{major}*

%files -n %{oldlib}
%{_libdir}/libpng.so.%{oldmajor}*

%changelog
* Sun Apr 01 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.49-1
+ Revision: 788555
- 1.2.49

* Tue Feb 21 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.47-1
+ Revision: 778674
- 1.2.47

* Fri Jan 27 2012 Antoine Ginies <aginies@mandriva.com> 2:1.2.46-8
+ Revision: 769274
- fix provides for lipng12-source

* Tue Dec 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.46-7
+ Revision: 738318
- drop the static lib and its sub package

* Thu Sep 15 2011 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2:1.2.46-6
+ Revision: 699918
- really fix the actual lib64 file conflict in libsdl12-config (d'oh)

* Thu Sep 15 2011 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2:1.2.46-5
+ Revision: 699911
- move autoreconf to %%prep, replacing autogen.sh
- fix pkgconfig file to avoid conflicts and avoid multiarch hackage (P3)
- make devel package able to co-exist with libpng15
- split really old libpng.so.3 into separate package

* Thu Sep 15 2011 Alexander Barakin <abarakin@mandriva.org> 2:1.2.46-4
+ Revision: 699867
- added automake buildrequires
- add autoreconf
- bump release
- removed uclibc conditions

  + Per Ã˜yvind Karlsen <peroyvind@mandriva.org>
    - fix missing epoch in conflicts

* Tue Sep 13 2011 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2:1.2.46-2
+ Revision: 699601
- remove duplicate/conflicting provides with lib64 issues...
- imported package libpng12


* Tue Sep 13 2011 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.46-2
- add back old version for compatibility

* Sat Jul 16 2011 Funda Wang <fwang@mandriva.org> 2:1.2.46-1mdv2011.0
+ Revision: 690109
- add apng patch
- new version 1.2.46

* Fri Apr 29 2011 Funda Wang <fwang@mandriva.org> 2:1.2.44-3
+ Revision: 660654
- update multiarch usage

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Sat Aug 14 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.44-2mdv2011.0
+ Revision: 569562
- sync with MDVSA-2010:133

* Fri Jul 09 2010 Funda Wang <fwang@mandriva.org> 2:1.2.44-1mdv2011.0
+ Revision: 549888
- New version 1.2.44

  + Oden Eriksson <oeriksson@mandriva.com>
    - remove the changelog (how did that happen?)

* Thu Feb 25 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.43-1mdv2010.1
+ Revision: 511259
- use a newer apng patch from upstream
- 1.2.43

* Wed Feb 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.42-1mdv2010.1
+ Revision: 510653
- 1.2.42
- rediffed the apng patch

  + Per Ã˜yvind Karlsen <peroyvind@mandriva.org>
    - make uclibc file in %%files conditional (thx to Matthew Dawkins for noticing!)

* Sat Dec 05 2009 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2:1.2.41-2mdv2010.1
+ Revision: 473715
- build with -fPIC

* Sat Dec 05 2009 Funda Wang <fwang@mandriva.org> 2:1.2.41-1mdv2010.1
+ Revision: 473664
- new version 1.2.41

  + Per Ã˜yvind Karlsen <peroyvind@mandriva.org>
    - compile with '-O3 -funroll-loops' (as suggested by upstream)
    - don't pass -DPNG_NO_MMX_CODE, it's already handled automatically by configure
    - build static uclibc linked library

* Sun Sep 13 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.40-1mdv2010.0
+ Revision: 439029
- update to new version 1.2.40

* Sun Aug 30 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.39-1mdv2010.0
+ Revision: 422506
- update to new version 1.2.39
- update patch0

* Sat Jun 06 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.37-1mdv2010.0
+ Revision: 383290
- update to new version 1.2.37
- Patch0: new version of apng patch

* Fri May 08 2009 Funda Wang <fwang@mandriva.org> 2:1.2.36-2mdv2010.0
+ Revision: 373374
- raise rel
- New version 1.2.36
- rediff p1

* Thu Feb 19 2009 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.35-1mdv2009.1
+ Revision: 342891
- 1.2.35

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.34-1mdv2009.1
+ Revision: 315702
- 1.2.34
- new P0

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.33-3mdv2009.1
+ Revision: 315590
- rebuild

* Wed Nov 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.33-2mdv2009.1
+ Revision: 300156
- added P1 to fix build problem with mysql-gui-tools-5.0r14

* Fri Oct 31 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.33-1mdv2009.1
+ Revision: 299045
- update to new version 1.2.33

* Sun Sep 21 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.32-1mdv2009.1
+ Revision: 286394
- update to noew version 1.2.32
- drop patch 1 as it is fixed upstream
- Patch0: new version

* Tue Sep 09 2008 Frederik Himpe <fhimpe@mandriva.org> 2:1.2.31-2mdv2009.0
+ Revision: 283256
- Add 1.2.31beta01 patch fixing buffer overflow CVE-2008-3964

* Sat Aug 23 2008 Funda Wang <fwang@mandriva.org> 2:1.2.31-1mdv2009.0
+ Revision: 275373
- update apng patch with archlinux

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 1.2.31
    - update to new version 1.2.30
    - use lzma'd tarball from upstream

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 2:1.2.29-2mdv2009.0
+ Revision: 264888
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 08 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.29-1mdv2009.0
+ Revision: 204605
- new version

* Fri May 02 2008 Frederik Himpe <fhimpe@mandriva.org> 2:1.2.28-1mdv2009.0
+ Revision: 200472
- New upstream version (fixes security issues)
- Run ./autogen.sh, like Debian is doing, otherwise it does not build
- Update apng patch to version which applies without problem, from
  SourceMage

* Tue Apr 15 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.25-3mdv2009.0
+ Revision: 193502
- update APNG patch

* Thu Feb 28 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.25-2mdv2008.1
+ Revision: 176548
- add support for APNG images, this is a mandatory for upcoming Firefox 3

* Tue Feb 19 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.25-1mdv2008.1
+ Revision: 172842
- new version
- remove docs from static library

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 26 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.24-1mdv2008.1
+ Revision: 137841
- new version
- new license policy

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 09 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.23-1mdv2008.1
+ Revision: 107203
- new version
- be more consistant on macros naming
- fix mixture of tabs and spaces
- some mino cleans in a spec file

* Sun Oct 14 2007 Funda Wang <fwang@mandriva.org> 2:1.2.22-1mdv2008.1
+ Revision: 98137
- New version 1.2.22

* Thu Oct 11 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.22-0.rc1.1mdv2008.1
+ Revision: 97198
- update to 1.2.22rc1 to close bug #34647

* Wed Oct 10 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.21-1mdv2008.1
+ Revision: 96614
- drop patch 0 and 1 since there is a configure script in use, which take care of everything
- remove dead entries in spec file
- let's see how libpng will work with mmx support on ix86
- new version
- new version

* Sat Aug 25 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.19-2mdv2008.0
+ Revision: 71324
- remove wrong obsoletes

* Sat Aug 25 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2:1.2.19-1mdv2008.0
+ Revision: 71212
- export -DPNG_NO_MMX_CODE for x86_64 arch
- correct requires and provides
- rediff patch 0
- new devel library policy
- drop patch 2 (there is better way)
- new version

* Mon Aug 06 2007 David Walluck <walluck@mandriva.org> 2:1.2.18-3mdv2008.0
+ Revision: 59535
- move %%{_mandir}/man5/* to devel package in order to avoid multiarch conflict

* Mon Jul 02 2007 Olivier Blin <oblin@mandriva.com> 2:1.2.18-2mdv2008.0
+ Revision: 47129
- add a libpng-source package (to be used for software rebuilding libpng, such as syslinux)
- remove obsolete conflicts

* Wed May 16 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2:1.2.18-1mdv2008.0
+ Revision: 27297
- Updated to 1.2.18.

* Fri Apr 20 2007 Olivier Blin <oblin@mandriva.com> 2:1.2.16-1mdv
+ Revision: 16258
- 1.2.16


* Sun Feb 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.2.13-2mdv2007.0
+ Revision: 122407
- fix buildrequires

* Fri Nov 17 2006 Olivier Blin <oblin@mandriva.com> 2:1.2.13-1mdv2007.1
+ Revision: 85128
- 1.2.13

* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.12-5mdv2007.1
+ Revision: 74600
- rebuild
- bzip2 cleanup
- rebuild

* Thu Oct 12 2006 Oden Eriksson <oeriksson@mandriva.com> 2:1.2.12-3mdv2007.1
+ Revision: 63449
- bunzip patches
- Import libpng

* Thu Aug 03 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.2.12-2mdv2007.0
- Drop broken x86_64 patches (including from #23692). Time to be spent
  for making the MMX code 64-bit safe is the same as writing correct
  SSE2+ code. And, without proper data for validating semantics and
  performance, this currently is not worth the effort for MDV2007.0
- Henceforth, make sure to enable MMX optimisations on 32-bit x86
  platforms only (Patch2)

* Sun Jul 02 2006 Giuseppe Ghibò <ghibo@mandriva.com> 1.2.12-1mdv2007.0
- Release 1.2.12.
- Added Patch2 from Alex Simon to allow Assembler support in pnggccrd.c
  (needs Gwenole review), to allow ImageMagick 6.2.8.1 building on X86-64.

* Sun Jun 18 2006 Warly <warly@mandriva.com>  1.2.10-4mdv2007.0
- This seem to be a desired behavior, need to recompile the packages requiring the old devel(libpng)

* Sun Jun 18 2006 Warly <warly@mandriva.com>  1.2.10-3mdv2007.0
- also workarround the problem for x86_64

* Sat Jun 17 2006 Warly <warly@mandriva.com>  1.2.10-2mdv2007.0
- workarround the non providing of devel(libpng)

* Fri Jun 16 2006 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 1.2.10-1mdv2007.0
- 1.2.10
- do configure
- %%mkrel
- regenerate P0 & P1
- move tests to new %%check stage
- multiarch

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.2.8-2mdk
- Rebuild

* Wed Dec 22 2004 Per Ã˜yvind Karlsen <peroyvind@linux-mandrake.com> 1.2.8-1mdk
- 1.2.8
- fix summary-ended-with-dot

* Tue Nov 09 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.2.7-1mdk
- new release

* Fri Oct 01 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.6-2mdk
- lib64 fixes to pkgconfig files

* Wed Aug 18 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.6-1mdk
- new release
- fix url
- kill patch 1 (merged upstream)

* Fri Jun 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2.5-11mdk
- security fix for CAN-2004-0421 (Vincent Danen)
- misc spec file fixes

