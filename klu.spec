%define NAME	KLU
%define major	1
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Name:		klu
Version:	1.2.1
Release:	2
Epoch:		1
Summary:	Routines for performing sparse LU factorization
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.cise.ufl.edu/research/sparse/klu/
Source0:	http://www.cise.ufl.edu/research/sparse/klu/%{NAME}-%{version}.tar.gz
BuildRequires:	amd-devel
BuildRequires:	btf-devel
BuildRequires:	camd-devel
BuildRequires:	ccolamd-devel
BuildRequires:	cholmod-devel
BuildRequires:	colamd-devel
BuildRequires:	suitesparse-common-devel >= 4.0.0

%description
KLU is a sparse LU factorization algorithm well-suited for use in
circuit simulation.

%package -n %{libname}
Summary:	Library of routines for performing sparse LU factorization
Group:		System/Libraries
%define	oldname	%{mklibname %{name} 1.2.1}
%rename		%{oldname}

%description -n %{libname}
KLU is a sparse LU factorization algorithm well-suited for use in
circuit simulation.

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{devname}
Summary:	C routines for performing sparse LU factorization
Group:		Development/C
Requires:	suitesparse-common-devel >= 4.0.0
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
KLU is a sparse LU factorization algorithm well-suited for use in
circuit simulation.

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c -n %{name}-%{version}
cd %{NAME}
find . -perm 0640 | xargs chmod 0644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
pushd Lib
    %make -f Makefile CC=gcc CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    gcc %{ldflags} -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lamd -lcolamd -lbtf -lcholmod -lm *.o
popd

%install
cd %{NAME}

for f in Lib/*.so*; do
    install -m755 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    install -m644 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    install -m644 $f -D %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Doc/*.txt Doc/*.pdf Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
