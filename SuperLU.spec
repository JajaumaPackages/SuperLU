%global genname superlu
%global majorver 5.1

Name:			SuperLU
Version:		5.1.1
Release:		2%{?dist}
Summary:		Subroutines to solve sparse linear systems
%{?el5:Group:		System/Libraries}

License:		BSD and GPLV2+
URL:			http://crd-legacy.lbl.gov/~xiaoye/SuperLU/
Source0:		http://crd-legacy.lbl.gov/~xiaoye/SuperLU/%{genname}_%{version}.tar.gz
# Build with -fPIC
Patch0:			%{genname}-511-add-fpic.patch
# Build shared library
Patch1:			%{genname}-511-build-shared-lib3.patch
# Fixes testsuite
Patch3:			%{genname}-511-fix-testsuite.patch
# remove non-free mc64 functionality
# patch obtained from the debian package
Patch4:			%{genname}-removemc64.patch

%{?el5:BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)}
BuildRequires:		atlas-devel
BuildRequires:		csh

%description
SuperLU contains a set of subroutines to solve a sparse linear system 
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). 
The columns of A may be preordered before factorization; the 
preordering for sparsity is completely separate from the factorization.

%package devel
Summary:		Header files and libraries for SuperLU development
%{?el5:Group:		Development/Libraries}
Requires:		%{name}%{?_isa}		=  %{version}-%{release}
%{?el5:Requires:	pkgconfig}

%description devel 
The %{name}-devel package contains the header files
and libraries for use with %{name} package.

%package doc
Summary:		Documentation and Examples for SuperLU
Requires:		%{name}%{?_isa} = %{version}-%{release}

%description doc
The %{name}-doc package contains all the help documentation along with C
and FORTRAN examples.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4

rm -fr SRC/mc64ad.f.bak
find . -type f | sed -e "/TESTING/d" | xargs chmod a-x
# Remove the shippped executables from EXAMPLE
find EXAMPLE -type f | while read file
do
   [ "$(file $file | awk '{print $2}')" = ELF ] && rm $file || :
done
cp -p MAKE_INC/make.linux make.inc
sed -i	-e "s|-O3|$RPM_OPT_FLAGS|"							\
	-e "s|\$(SUPERLULIB) ||"							\
	-e "s|\$(HOME)/Dropbox/Codes/%{name}/%{name}|%{_builddir}/%{name}_%{version}|"	\
	-e 's!lib/libsuperlu_5.1.a$!SRC/libsuperlu.so!'					\
	-e 's!-shared!& %{__global_ldflags}!'						\
%if 0%{?fedora} >= 21
	-e "s|-L/usr/lib -lblas|-L%{_libdir}/atlas -lsatlas|"				\
%else
	-e "s|-L/usr/lib -lblas|-L%{_libdir}/atlas -lf77blas|"				\
%endif
	make.inc

%build
make %{?_smp_mflags} superlulib
make -C TESTING

%install
%{?el5:rm -rf %{buildroot}}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
install -p SRC/libsuperlu.so.%{majorver} %{buildroot}%{_libdir}
install -p SRC/*.h %{buildroot}%{_includedir}/%{name}
chmod -x %{buildroot}%{_includedir}/%{name}/*.h
cp -Pp SRC/libsuperlu.so %{buildroot}%{_libdir}

%check
pushd TESTING
for _test in c d s z
do
  chmod +x ${_test}test.csh
  ./${_test}test.csh
done
popd

%{?el5:%clean}
%{?el5:rm -rf %{buildroot}}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README
%{_libdir}/libsuperlu.so.%{majorver}

%files devel
%{_includedir}/%{name}/
%{_libdir}/libsuperlu.so

%files doc
%doc DOC EXAMPLE FORTRAN

%changelog
* Mon Mar 28 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 5.1.1-2
- Added -doc subpackage
- Added GPLv2 in the license field

* Mon Mar 21 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 5.1.1-1
- Update to 5.1.1
- Remove format security patch - not needed anymore
- Edit patches to be version specific
- Renamed patch4 to be consistent with others
- Minor spec file housekeeping

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 25 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.3-12
- Fix spec file errors and remove backup files
- fixes 1084707

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 13 2014 Mukundan Ragavan <nonamedotc@gmail.com> - 4.3-10
- Removed non-free files, fixes bz#1114264

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 06 2014 Björn Esser <bjoern.esser@gmail.com> - 4.3-8
- fixed FTBFS if "-Werror=format-security" flag is used (#1037343)
- devel-pkg must Requires: %%{name}%%{?_isa}
- apply proper LDFLAGS
- added needed bits for el5
- reenable testsuite using Patch3

* Fri Oct 4 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3-7
- Rebuild for atlas 3.10
- Handle UnversionedDocDirs change

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-5
- Ship SuperLU examples

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-3
- Use README in main package and DOC in devel package
- chmod a-x on SRC/qselect.c
- Remove -latlas linking in prep section
- Added Patch comments
- Use name RPM macro in patch name

* Wed Feb 01 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-2
- Use atlas library instead of blas.
- Use RPM_OPT_FLAGS and LIBS when building sources.
- Use macros as required for name and version.

* Fri Jan 06 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 4.3-1
- First release.
