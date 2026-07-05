%global commit          2be5e68b202a37037330a90765ea76a63b6a3421
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global upstreamname    noctalia

Name:   	noctalia-git
Version:	5.0.0
Release:	0.248.git%{shortcommit}%{?dist}
Summary:	A lightweight Wayland shell and bar built directly on Wayland + OpenGL ES, with no Qt or GTK dependency.

License:	MIT
URL:		https://github.com/noctalia-dev/%{upstreamname}
Source0:	%{url}/archive/%{commit}/%{upstreamname}-%{commit}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  desktop-file-utils
BuildRequires:  md4c-devel
BuildRequires:  tomlplusplus-devel
BuildRequires:  pipewire-devel
BuildRequires:  wireplumber-devel
BuildRequires:  sdbus-cpp-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libqalculate)  
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

Provides:       desktop-notification-daemon
Provides:       PolicyKit-authentication-agent

Requires:       hicolor-icon-theme
Requires:       dejavu-sans-fonts
Requires:       libwebp

Recommends:     ddcutil
Recommends:     gpu-screen-recorder
Recommends:     power-profiles-daemon

%description
%{summary}

%prep
%autosetup -n %{upstreamname}-%{commit}
# Manually insert commit hash
sed -i "s/'unknown'/'%{shortcommit}'/g" meson.build

# Remove bundled libs that we have system copies of
rm -r third_party/tomlplusplus
rm -r third_party/md4c

%build
%meson \
	 -Dsystem_tomlplusplus=true \
	 -Dsystem_md4c=true \
%meson_build

%install
%meson_install
install -d %{buildroot}%{_licensedir}/%{name}/third_party
find third_party -type f \( -name "LICENSE*" -o -name "COPYING*" -o -name "NOTICE*" \) | while read -r file; do
    # Create the destination subdirectory
    dest_dir="%{buildroot}%{_licensedir}/%{name}/$(dirname "$file")"
    install -d "$dest_dir"
    # Copy the file to its specific subfolder
    install -p -m 0644 "$file" "$dest_dir/"
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/dev.noctalia.Noctalia.desktop

%files
%doc README.md
%license LICENSE
%{_licensedir}/%{name}/third_party/
%{_bindir}/noctalia
%{_datadir}/noctalia/
%{_datadir}/applications/dev.noctalia.Noctalia.desktop
%{_datadir}/icons/hicolor/scalable/apps/noctalia.svg

%changelog
%autochangelog
