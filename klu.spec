%define epoch		0

%define name		klu
%define NAME		KLU
%define version		1.0.1
%define release		%mkrel 1
%define major		%{version}
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Routines for solving unsymmetric sparse linear systems
Group:		System/Libraries
License:	LGPL
URL:		http://www.cise.ufl.edu/research/sparse/umfpack/
Source0:	http://www.cise.ufl.edu/research/sparse/umfpack/%{NAME}-%{version}.tar.gz
Source1:	http://www.cise.ufl.edu/research/sparse/ufconfig/UFconfig-3.1.0.tar.gz
BuildRequires:	amd-devel >= 2.0.0, colamd-devel >= 2.0.0, btf-devel >= 1.0.0
BuildRequires:	camd-devel >= 2.0.0, ccolamd-devel >= 2.0.0
BuildRequires:	cholmod-devel >= 1.0.0
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description

%package -n %{libname}
Summary:	Library of routines for solving unsymmetric sparse linear systems
Group:		System/Libraries
Provides:	%{libname} = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname %name 1

%description -n %{libname}

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{develname}
Summary:	C routines for solving unsymmetric sparse linear systems
Group:		Development/C
Requires:	suitesparse-common-devel >= 3.0.0
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes: 	%mklibname %name 1 -d

%description -n %{develname}

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c 
%setup -q -c -a 0 -a 1
%setup -q -D -T -n %{name}-%{version}/%{NAME}

%build
pushd Lib
    %make -f Makefile CC=%__cc CFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/suitesparse" INC=
    %__cc -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lamd -lcolamd -lbtf -lcholmod -lm *.o
popd

%install
%__rm -rf %{buildroot}

%__install -d -m 755 %{buildroot}%{_libdir} 
%__install -d -m 755 %{buildroot}%{_includedir}/suitesparse 

for f in Lib/*.so*; do
    %__install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    %__install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    %__install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

%__ln_s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

%__install -d -m 755 %{buildroot}%{_docdir}/%{name}
%__install -m 644 README.txt Doc/*.txt Doc/*.pdf Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%clean
%__rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_docdir}/%{name}
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
