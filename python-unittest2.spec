#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	tests	# test target

Summary:	New features in unittest backported to older Python versions
Summary(pl.UTF-8):	Backport nowych funkcji modułu unittest do starszych wersji Pythona
Name:		python-unittest2
Version:	1.1.0
Release:	1
License:	MIT
Group:		Development/Tools
#Source0Download: https://pypi.python.org/simple/unittest2/
Source0:	https://pypi.python.org/packages/source/u/unittest2/unittest2-%{version}.tar.gz
# Source0-md5:	f72dae5d44f091df36b6b513305ea000
URL:		https://pypi.python.org/pypi/unittest2
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
%if "%{py_ver}" < "2.7"
BuildRequires:	python-argparse
%endif
BuildRequires:	python-six >= 1.4
BuildRequires:	python-traceback2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-six >= 1.4
BuildRequires:	python3-traceback2
%endif
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-six >= 1.4
Requires:	python-traceback2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
unittest2 is a backport of the new features added to the unittest
testing framework in Python 2.7 and onwards.

%description -l pl.UTF-8
unittest2 to backport nowych funkcji dodanych do szkieletu testów
unittest w Pythonie 2.7 i nowszych.

%package -n python3-unittest2
Summary:	New features in unittest backported to older Python versions
Summary(pl.UTF-8):	Backport nowych funkcji modułu unittest do starszych wersji Pythona
Group:		Development/Tools
Requires:	python3-six >= 1.4
Requires:	python3-traceback2

%description -n python3-unittest2
unittest2 is a backport of the new features added to the unittest
testing framework in Python 2.7 and onwards.

%description -n python3-unittest2 -l pl.UTF-8
unittest2 to backport nowych funkcji dodanych do szkieletu testów
unittest w Pythonie 2.7 i nowszych.

%prep
%setup -q -n unittest2-%{version}

%if "%{py_ver}" >= "2.7"
# argparse is in base distribution
%{__sed} -i -e "/^REQUIRES/s@'argparse', @@" setup.py
%endif

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/unit2{,-2}

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/unittest2/test
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/unit2{,-3}

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/unittest2/test
%endif

%if %{with python2}
ln -sf unit2-2 $RPM_BUILD_ROOT%{_bindir}/unit2
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/unit2
%attr(755,root,root) %{_bindir}/unit2-2
%dir %{py_sitescriptdir}/unittest2
%{py_sitescriptdir}/unittest2/*.py[co]
%{py_sitescriptdir}/unittest2-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-unittest2
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/unit2-3
%dir %{py3_sitescriptdir}/unittest2
%{py3_sitescriptdir}/unittest2/*.py
%{py3_sitescriptdir}/unittest2/__pycache__
%{py3_sitescriptdir}/unittest2-%{version}-py*.egg-info
%endif