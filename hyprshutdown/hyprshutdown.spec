%global commit 4f3278e180e69160e0456f673635741a9cea6548
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:    hyprshutdown
Version: 0
Release: 1.git%{shortcommit}%{?dist}
Summary: A graceful shutdown utility for Hyprland
License: BSD-3-Clause license
URL:     https://github.com/hyprwm/hyprshutdown

Source: %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

Patch:	cmakelists-remove-desktop-file.patch

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: glaze-devel
BuildRequires: pkgconfig(hyprlang)
BuildRequires: pkgconfig(hyprutils)
BuildRequires: pkgconfig(hyprtoolkit)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(pixman-1)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: systemd-devel

Requires: (hyprland or hyprland-git)
Requires: systemd

%description
hyprshutdown is a graceful shutdown/logout utility for Hyprland, which prevents apps from crashing / dying unexpectedly..

%prep
%autosetup -n %{name}-%{commit} -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/hyprshutdown

%changelog
* Fri Dec 05 2025 LionHeartP <LionHeartP@proton.me> - 0-1.git4f3278e
- Initial package
