%global commit          db60c06b5f6ff5da4d5f1126eff312b2a41ef614
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:   	noctalia-greeter
Version:	1.0.0
Release:	0.1.git%{shortcommit}%{?dist}
Summary:	A minimal login greeter for greetd that matches the look and feel of Noctalia Shell.

License:	MIT
URL:		https://github.com/noctalia-dev/%{name}
Source0:	%{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  cage
BuildRequires:  dbus
BuildRequires:  gcc-c++
BuildRequires:  greetd
BuildRequires:  just
BuildRequires:  meson
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
BuildRequires:  wlr-randr

Requires:       cage
Requires:       dbus
Requires:       greetd

%description
%{summary}

%prep
%autosetup -n %{name}-%{commit}

%build
export LDFLAGS="%{__global_ldflags} -Wl,-z,notext"
%meson
%meson_build

%install
%meson_install
# No third party licenses implemented yet
#install -d %{buildroot}%{_licensedir}/%{name}/third_party
#find third_party -type f \( -name "LICENSE*" -o -name "COPYING*" -o -name "NOTICE*" \) | while read -r file; do
    # Create the destination subdirectory
#    dest_dir="%{buildroot}%{_licensedir}/%{name}/$(dirname "$file")"
#    install -d "$dest_dir"
#    # Copy the file to its specific subfolder
#    install -p -m 0644 "$file" "$dest_dir/"
#done

%files
%doc README.md
%license LICENSE
#%%{_licensedir}/%%{name}/third_party/
%{_bindir}/%{name}
%{_bindir}/%{name}-apply-appearance
%{_bindir}/%{name}-print-greetd-config
%{_bindir}/%{name}-session
%{_datadir}/%{name}/*
%{_datadir}/polkit-1/actions/org.noctalia.greeter.apply-appearance.policy

%changelog
%autochangelog
