%global commit          a5fd79c1da0a079c29b36cd9d27df6a7db4b8bfa
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global buildrevision   %(c=%{commit}; echo ${c:0:9})
%global upstreamname    luciole
%global upstreamurl     https://github.com/noctalia-dev/%{upstreamname}

Name:           luciole-git
Version:        0.1.0^2.%{shortcommit}
Release:        1%{?dist}
Summary:        Native Wayland file manager with fast previews, tabs and split view

License:        MIT
URL:            %{upstreamurl}
Source0:        %{upstreamurl}/archive/%{commit}/%{upstreamname}-%{commit}.tar.gz

ExcludeArch:    %{ix86}

BuildRequires:  gcc-c++
BuildRequires:  meson >= 1.1
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel >= 1.49
BuildRequires:  libacl-devel
BuildRequires:  libarchive-devel
BuildRequires:  xz-devel
BuildRequires:  libpng-devel
BuildRequires:  librsvg2-devel
BuildRequires:  tomlplusplus-devel >= 3.4
BuildRequires:  json-devel
BuildRequires:  stb_image_resize2-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(pango) >= 1.50
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(glib-2.0) >= 2.76
BuildRequires:  pkgconfig(gio-2.0) >= 2.76
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.76
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.44
BuildRequires:  pkgconfig(glycin-2) >= 2.0.1
BuildRequires:  pkgconfig(tomlplusplus) >= 3.4
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libxml-2.0)

Requires:       gvfs
Requires:       shared-mime-info
Requires:       gsettings-desktop-schemas
Requires:       dconf

Recommends:     adwaita-icon-theme
Recommends:     hicolor-icon-theme
Recommends:     glycin-loaders
Recommends:     glib-networking

Suggests:       ffmpeg-free
Suggests:       ffmpegthumbnailer
Suggests:       poppler-utils
Suggests:       7zip
Suggests:       gvfs-smb
Suggests:       xdg-terminal-exec
Suggests:       xdg-desktop-portal

Conflicts:      luciole
# Terra
Conflicts:      luciole-nightly

%description
Luciole, a native Wayland file manager using Noctalia rendering and controls (in development)

%prep
%autosetup -n %{upstreamname}-%{commit}

%build
%meson \
    --buildtype=release \
    -Db_ndebug=true \
    -Dtests=disabled \
    -Dnative_optimizations=false \
    -Dbuild_revision=%{buildrevision}
%meson_build

%install
%meson_install

%files
%doc README.md PACKAGING.md
%license %{_datadir}/licenses/luciole/LICENSE
%license %{_datadir}/luciole/assets/fonts/tabler-icons-license.txt
%{_bindir}/luciole
%{_datadir}/applications/dev.noctalia.luciole.desktop
%{_datadir}/bash-completion/completions/luciole
%{_datadir}/dbus-1/services/dev.noctalia.luciole.FileManager1.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.luciole.service
%{_datadir}/fish/vendor_completions.d/luciole.fish
%{_datadir}/icons/hicolor/scalable/apps/dev.noctalia.luciole.svg
%{_datadir}/luciole/assets/fonts/noctalia-tabler.ttf
%{_datadir}/luciole/assets/fonts/tabler.json
%{_datadir}/luciole/templates/colors.toml
%{_datadir}/xdg-desktop-portal/portals/luciole.portal
%{_datadir}/zsh/site-functions/_luciole

%changelog
%autochangelog
