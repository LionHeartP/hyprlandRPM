%global commit          74e6c2790dd8f39bf496e90e479a9ae370846eed
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global upstreamname    noctalia

Name:   	noctalia-git
Version:	5.0.0^413.%{shortcommit}
Release:	1%{?dist}
Summary:	A sleek, customizable desktop shell crafted for Wayland.

License:	MIT
URL:		https://github.com/noctalia-dev/%{upstreamname}
Source0:	%{url}/archive/%{commit}/%{upstreamname}-%{commit}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  desktop-file-utils
BuildRequires:  json-devel
BuildRequires:  md4c-devel
BuildRequires:  pipewire-devel
BuildRequires:  sdbus-cpp-devel
BuildRequires:  stb-devel
BuildRequires:  tomlplusplus-devel
BuildRequires:  wireplumber-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libjxl_cms)
BuildRequires:  pkgconfig(libical)
BuildRequires:  pkgconfig(libqalculate)  
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsodium)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(sndfile)
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

Conflicts:      noctalia

%description
%{summary}

%package bash-completion
Summary:        Bash completion for %{upstreamname}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} = %{version}-%{release} and bash-completion)

%description bash-completion
Bash command-line completion support for %{upstreamname}.

%package zsh-completion
Summary:        Zsh completion for %{upstreamname}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} = %{version}-%{release} and zsh)

%description zsh-completion
Zsh command-line completion support for %{upstreamname}.

%package fish-completion
Summary:        Fish completion for %{upstreamname}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       fish
Supplements:    (%{name} = %{version}-%{release} and fish)

%description fish-completion
Fish command-line completion support for %{upstreamname}.

%prep
%autosetup -n %{upstreamname}-%{commit}
# Manually insert commit hash
sed -i "s/'unknown'/'%{shortcommit}'/g" meson.build

%build
%meson \
  --buildtype=release \
  -Db_lto=true
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

# Generate and install shell completions
install -d %{buildroot}%{_datadir}/bash-completion/completions
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -d %{buildroot}%{_datadir}/fish/vendor_completions.d

%{_vpath_builddir}/noctalia completions bash > %{buildroot}%{_datadir}/bash-completion/completions/noctalia
%{_vpath_builddir}/noctalia completions zsh  > %{buildroot}%{_datadir}/zsh/site-functions/_noctalia
%{_vpath_builddir}/noctalia completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/noctalia.fish

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

%files bash-completion
%{_datadir}/bash-completion/completions/noctalia

%files zsh-completion
%{_datadir}/zsh/site-functions/_noctalia

%files fish-completion
%{_datadir}/fish/vendor_completions.d/noctalia.fish

%changelog
%autochangelog
