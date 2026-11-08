%bcond wireplumber %[0%{?fedora} > 39]

%global commit0 567368cbd3ef0fc02ffdcb7085e1618014432aab
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 2

Name:           waybar-git
Version:        0.16.0%{?bumpver:^%{bumpver}.git%{shortcommit0}}
Release:        1%{?dist}
Summary:        Highly customizable Wayland bar for Sway and Wlroots based compositors, with workspaces support for Hyprland
# Source files/overall project licensed as MIT, but
# - BSL-1.0
#   * include/util/clara.hpp
# - HPND-sell-variant
#   * protocol/ext-workspace-unstable-v1.xml
#   * protocol/wlr-foreign-toplevel-management-unstable-v1.xml
#   * protocol/wlr-layer-shell-unstable-v1.xml
# - ISC
#   * protocol/river-control-unstable-v1.xml
#   * protocol/river-status-unstable-v1.xml
#   * src/util/rfkill.cpp
License:        MIT AND BSL-1.0 AND ISC
URL:            https://github.com/Alexays/Waybar
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.49.0
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros
%if %{fedora} >= 40
BuildRequires:  pkgconfig(catch2)
%endif
BuildRequires:  pkgconfig(date)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(fmt) >= 8.1.1
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0)
BuildRequires:  pkgconfig(gtkmm-3.0)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libmpdclient)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libnl-genl-3.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(mm-glib)
BuildRequires:  pkgconfig(playerctl)
BuildRequires:  pkgconfig(sigc++-2.0)
BuildRequires:  pkgconfig(spdlog) >= 1.10.0
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
%if %{with wireplumber}
BuildRequires:  pkgconfig(wireplumber-0.5)
%endif
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(xkbregistry)
BuildRequires:  python3dist(packaging)
BuildRequires:  pkgconfig(libgps)

Conflicts:      waybar
Provides:       waybar

Enhances:       hyprland
Recommends:     (font(fontawesome6free) or font(fontawesome5free))

%description
%{summary}.

%prep
%autosetup -p1 -n Waybar-%{commit0}

%build
%meson \
%if %{fedora} < 40
    -Dtests=disabled \
%endif
    -Dsndio=disabled \
    -Dcava=disabled \
    %{!?with_wireplumber:-Dwireplumber=disabled}
%meson_build

%install
%meson_install
# remove man pages for disabled modules
for module in cava sndio %{!?with_wireplumber:wireplumber} wlr-workspaces; do
    rm -f %{buildroot}%{_mandir}/man5/%{name}-${module}.5
done

%check
%meson_test

%post
%systemd_user_post waybar.service

%preun
%systemd_user_preun waybar.service


%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/xdg/waybar
%config(noreplace) %{_sysconfdir}/xdg/waybar/config.jsonc
%config(noreplace) %{_sysconfdir}/xdg/waybar/style.css
%{_bindir}/waybar
%{_libdir}/waybar/waybar-gps.so
%{_mandir}/man5/waybar*
%{_userunitdir}/waybar.service

%changelog
%autochangelog
