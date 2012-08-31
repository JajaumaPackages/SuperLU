Name:           SuperLU
Version:        4.3
Release:        3%{?dist}
Summary:        Subroutines to solve sparse linear systems

License:        BSD
URL:            http://crd-legacy.lbl.gov/~xiaoye/SuperLU/
Source0:        http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_%{version}.tar.gz
# Build with -fPIC
Patch0:         %{name}-add-fpic.patch
# Build shared library
Patch1:         %{name}-build-shared-lib3.patch


BuildRequires:  atlas-devel
BuildRequires:  csh

%description
SuperLU contains a set of subroutines to solve a sparse linear system 
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). 
The columns of A may be preordered before factorization; the 
preordering for sparsity is completely separate from the factorization.

%package devel
Summary:        Header files and libraries for SuperLU development
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel 
The %{name}-devel package contains the header files
and libraries for use with CUnit package.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1
%patch1 -p1
chmod a-x SRC/qselect.c 
cp -p MAKE_INC/make.linux make.inc
sed -i "s|-O3|$RPM_OPT_FLAGS|" make.inc
sed -i "s|\$(SUPERLULIB) ||" make.inc
sed -i "s|\$(HOME)/Codes/%{name}_%{version}|%{_builddir}/%{name}_%{version}|" make.inc
sed -i "s|-L/usr/lib -lblas|-L%{_libdir}/atlas -lf77blas|" make.inc

%build
make %{?_smp_mflags} superlulib

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
install -p SRC/libsuperlu.so.%{version} %{buildroot}%{_libdir}
install -p SRC/*.h %{buildroot}%{_includedir}/%{name}
chmod -x %{buildroot}%{_includedir}/%{name}/*.h
cp -Pp SRC/libsuperlu.so %{buildroot}%{_libdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libsuperlu.so.*

%files devel
%defattr(-,root,root,-)
%doc DOC
%{_includedir}/%{name}/
%{_libdir}/libsuperlu.so

%changelog
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
