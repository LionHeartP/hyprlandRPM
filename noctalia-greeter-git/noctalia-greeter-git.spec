%global commit          8c97c04329e4cf73c6e5b9318be2f088b9b4a399
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global upstreamname    noctalia-greeter

Name:   	noctalia-greeter-git
Version:	1.3.1^4.%{shortcommit}
Release:	1%{?dist}
Summary:	A minimal login greeter for greetd that matches the look and feel of Noctalia Shell.

License:	MIT
URL:		https://github.com/noctalia-dev/%{upstreamname}
Source0:	%{url}/archive/%{commit}/%{upstreamname}-%{commit}.tar.gz

BuildRequires:  dbus
BuildRequires:  gcc-c++
BuildRequires:  greetd
BuildRequires:  json-devel
BuildRequires:  just
BuildRequires:  meson
BuildRequires:  stb-devel
BuildRequires:  tomlplusplus-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  polkit
BuildRequires:  wlroots-devel >= 0.20

Requires:       dbus
Requires:       greetd
Requires:       wlroots >= 0.20

Conflicts:      noctalia-greeter

%description
%{summary}

%prep
%autosetup -n %{upstreamname}-%{commit}

%build
%meson -Db_pie=true
%meson_build

%install
%meson_install
# Delete the unneeded tmpfiles.d fallback configuration
rm -f %{buildroot}%{_tmpfilesdir}/noctalia-greeter.conf
install -d %{buildroot}%{_licensedir}/%{upstreamname}/third_party
find third_party -type f \( -name "LICENSE*" -o -name "COPYING*" -o -name "NOTICE*" \) | while read -r file; do
    # Create the destination subdirectory
    dest_dir="%{buildroot}%{_licensedir}/%{upstreamname}/$(dirname "$file")"
    install -d "$dest_dir"
    # Copy the file to its specific subfolder
    install -p -m 0644 "$file" "$dest_dir/"
done

%files
%doc README.md
%license LICENSE
%{_licensedir}/%{upstreamname}/third_party/
%{_bindir}/%{upstreamname}
%{_bindir}/%{upstreamname}-apply-appearance
%{_bindir}/%{upstreamname}-compositor
%{_bindir}/%{upstreamname}-print-greetd-config
%{_bindir}/%{upstreamname}-session
%{_datadir}/%{upstreamname}/*
%{_datadir}/polkit-1/actions/org.noctalia.greeter.apply-appearance.policy

%changelog
%autochangelog
