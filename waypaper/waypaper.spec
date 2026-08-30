Name:           waypaper
Version:        2.9
Release:        %autorelease
Summary:        GUI wallpaper setter for Wayland

License:        GPL-3.0-or-later
URL:            https://github.com/anufrievroman/%{name}
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel

Recommends:     awww

%description
GUI wallpaper setter for Wayland and Xorg window managers. It works as
a frontend for popular wallpaper backends like swaybg, awww, wallutils and feh.

%prep
%autosetup -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{name}

# Move systemd unit file to standard location
mkdir -p %{buildroot}%{_userunitdir}
mv %{buildroot}%{_datadir}/systemd/user/%{name}d.service %{buildroot}%{_userunitdir}/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}d
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/man/man1/%{name}.1.*
%{_userunitdir}/%{name}d.service

%changelog
%autochangelog
