%global _default_patch_fuzz 2

Name:   	noctalia-shell
Version:	3.0.9
Release:	%autorelease
Summary:	A sleek and minimal desktop shell thoughtfully crafted for Wayland, built with Quickshell.

License:	MIT
URL:		https://github.com/noctalia-dev/%{name}
Source0:	%{url}/releases/download/v%{version}/noctalia-v%{version}.tar.gz

Patch0:		0001-revert-SystemMonitor-remove-GPU-temp.patch
Patch1: 	0001-Hyprland-use-uwsm-logout-function.patch

BuildArch:	noarch

Requires:	brightnessctl
Requires:	dejavu-sans-fonts
Requires:	google-roboto-fonts
Requires:	gpu-screen-recorder
Requires:	quickshell
Requires:	rsms-inter-fonts

Recommends:	cava
Recommends:	cliphist
Recommends:	ddcutil
Recommends:	matugen
Recommends:	power-profiles-daemon
Recommends:	wlsunset

%description
%{summary}

%prep
%autosetup -n noctalia-release -p1

%build

%install
install -d -m 0755 %{buildroot}/etc/xdg/quickshell/noctalia-shell
cp -r ./* %{buildroot}/etc/xdg/quickshell/noctalia-shell/

%files
%doc README.md
%license LICENSE
%{_sysconfdir}/xdg/quickshell/noctalia-shell/

%changelog
* Tue Nov 11 2025 LionHeartP <LionHeartP@proton.me> - 3.0.9-1
- Update to 3.0.9

* Mon Nov 10 2025 LionHeartP <LionHeartP@proton.me> - 3.0.6-1
- Update to 3.0.6

* Sun Nov 09 2025 LionHeartP <LionHeartP@proton.me> - 3.0.2-2
- Hyprland Service: Add patch to logout using uwsm

* Sat Nov 08 2025 LionHeartP <LionHeartP@proton.me> - 3.0.2-1
- Update to 3.0.2

* Fri Nov 07 2025 LionHeartP <LionHeartP@proton.me> - 3.0.0-1
- Update to 3.0.0

* Sat Nov 01 2025 LionHeartP <LionHeartP@proton.me> - 2.21.1-1
- Update to 2.21.1

* Fri Oct 31 2025 LionHeartP <LionHeartP@proton.me> - 2.21.0-1
- Update to 2.21.0

* Thu Oct 30 2025 LionHeartP <LionHeartP@proton.me> - 2.20.0-1
- Update to 2.20.0

* Tue Oct 21 2025 LionHeartP <LionHeartP@proton.me> - 2.19.0-2
- Change ddcutil to soft dep

* Tue Oct 21 2025 LionHeartP <LionHeartP@proton.me> - 2.19.0-1
- Update to 2.19.0

* Fri Oct 17 2025 LionHeartP <LionHeartP@proton.me> - 2.18.2-1
- Update to 2.18.2

* Fri Oct 17 2025 LionHeartP <LionHeartP@proton.me> - 2.18.1-1
- Update to 2.18.1

* Wed Oct 15 2025 LionHeartP <LionHeartP@proton.me> - 2.18.0-2
- Update GPU temp patch with new style code from upstream

* Wed Oct 15 2025 LionHeartP <LionHeartP@proton.me> - 2.18.0-1
- Update to 2.18.0

* Sun Oct 12 2025 LionHeartP <LionHeartP@proton.me> - 2.17.3-1
- Initial RPM release based on Arch PKGBUILD.
