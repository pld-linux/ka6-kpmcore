#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.2
%define		kframever	6.13.0
%define		qtver		6.8
%define		kaname		kpmcore
Summary:	KPMcore
Name:		ka6-%{kaname}
Version:	25.08.2
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	99ba7811140670f3cbc8896cd0bd0b23
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel
BuildRequires:	Qt6Gui-devel >= 5.12.3
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	polkit-qt6-1-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
Conflicts:	kde4-libksane >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KPMcore is a library for examining and manipulating all facets of
storage devices on a system:
- raw disk devices
- partition tables on a device
- filesystems within a partition

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libkpmcore.so.1?
%attr(755,root,root) %{_libdir}/libkpmcore.so.*.*
%dir %{_libdir}/qt6/plugins/kpmcore
%attr(755,root,root) %{_libdir}/qt6/plugins/kpmcore/pmdummybackendplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kpmcore/pmsfdiskbackendplugin.so
%attr(755,root,root) %{_prefix}/libexec/kpmcore_externalcommand
%{_datadir}/dbus-1/system-services/org.kde.kpmcore.helperinterface.service
%{_datadir}/dbus-1/system.d/org.kde.kpmcore.helperinterface.conf
%{_datadir}/polkit-1/actions/org.kde.kpmcore.externalcommand.policy

%files devel
%defattr(644,root,root,755)
%{_includedir}/kpmcore
%{_libdir}/cmake/KPMcore
%{_libdir}/libkpmcore.so
