%bcond_with         asan

Name:               noctalia-qs
Version:            0.0.2
Release:            %autorelease
Summary:            Fork of Quickshell - a flexible QtQuick based desktop shell toolkit

License:            LGPL-3.0-only AND GPL-3.0-only
URL:                https://github.com/noctalia-dev/noctalia-qs
Source:             %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:      breakpad-static
BuildRequires:      cmake
BuildRequires:      cmake(Qt6Core)
BuildRequires:      cmake(Qt6Qml)
BuildRequires:      cmake(Qt6ShaderTools)
BuildRequires:      cmake(Qt6WaylandClient)
BuildRequires:      gcc-c++
BuildRequires:      ninja-build
BuildRequires:      pkgconfig(breakpad)
BuildRequires:      pkgconfig(CLI11)
BuildRequires:      pkgconfig(gbm)
BuildRequires:      pkgconfig(glib-2.0)
BuildRequires:      pkgconfig(jemalloc)
BuildRequires:      pkgconfig(libdrm)
BuildRequires:      pkgconfig(libpipewire-0.3)
BuildRequires:      pkgconfig(pam)
BuildRequires:      pkgconfig(polkit-agent-1)
BuildRequires:      pkgconfig(wayland-client)
BuildRequires:      pkgconfig(wayland-protocols)
BuildRequires:      qt6-qtbase-private-devel
BuildRequires:      spirv-tools

%if %{with asan}
BuildRequires:      libasan
%endif

Conflicts:          quickshell
Provides:           desktop-notification-daemon
Obsoletes:          quickshell <= 0.2.2

%description
noctalia-qs is a custom fork of Quickshell — a flexible QtQuick-based desktop shell toolkit for Wayland. It serves as the shell framework powering Noctalia Shell.

%prep
%autosetup

%build
%cmake  -GNinja \
%if %{with asan}
        -DASAN=ON \
%endif
        -DBUILD_SHARED_LIBS=OFF \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr noctalia-qs \
        -DDISTRIBUTOR="Fedora COPR (lionheartp/Hyprland)" \
        -DDISTRIBUTOR_DEBUGINFO_AVAILABLE=YES \
        -DGIT_REVISION=%{commit} \
        -DINSTALL_QML_PREFIX=%{_lib}/qt6/qml
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%license LICENSE-GPL
%doc BUILD.md
%doc CONTRIBUTING.md
%doc README.md
#%%doc changelog/v%%{version}.md
%{_bindir}/qs
%{_datadir}/applications/dev.noctalia.%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/dev.noctalia.%{name}.svg
%{_libdir}/qt6/qml/Quickshell

%changelog
%autochangelog
