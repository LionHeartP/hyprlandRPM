Name:   	noctalia-shell
Version:	4.3.0
Release:	%autorelease
Summary:	A sleek and minimal desktop shell thoughtfully crafted for Wayland, built with Quickshell.

License:	MIT
URL:		https://github.com/noctalia-dev/%{name}
Source0:	%{url}/releases/download/v%{version}/noctalia-v%{version}.tar.gz

BuildArch:	noarch

Requires:	brightnessctl
Requires:	dejavu-sans-fonts
Requires:	qt6-qtmultimedia
Requires:	quickshell
Requires:	ImageMagick

Recommends:	cava
Recommends:	cliphist
Recommends:	ddcutil
Recommends:	gpu-screen-recorder
Recommends:	power-profiles-daemon
Recommends:	wlsunset

%description
%{summary}

%prep
%autosetup -n noctalia-release

%build

%install
install -d -m 0755 %{buildroot}/etc/xdg/quickshell/noctalia-shell
cp -r ./* %{buildroot}/etc/xdg/quickshell/noctalia-shell/

%files
%doc README.md
%license LICENSE
%{_sysconfdir}/xdg/quickshell/noctalia-shell/

%changelog
%autochangelog
