%global commit 813bd56e2c2644ae55759f09f65669abf7be03ce
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:    hyprshutdown
Version: 0
Release: 4.git%{shortcommit}%{?dist}
Summary: A graceful shutdown utility for Hyprland
License: BSD-3-Clause license
URL:     https://github.com/hyprwm/hyprshutdown

Source: %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires: 	gcc-c++
BuildRequires: 	cmake
BuildRequires: 	glaze-devel
BuildRequires: 	pkgconfig(hyprlang)
BuildRequires: 	pkgconfig(hyprutils)
BuildRequires: 	pkgconfig(hyprtoolkit)
BuildRequires: 	pkgconfig(libdrm)
BuildRequires: 	pkgconfig(pixman-1)
BuildRequires: 	pkgconfig(wayland-client)
BuildRequires: 	systemd-devel

Requires:	(hyprland or hyprland-git)
Requires:	systemd

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
