Name:           hyprmod
Version:        0.4.0
Release:        %autorelease -b2
Summary:        Native GTK4/libadwaita settings app for Hyprland

License:        GPL-3.0-or-later
URL:            https://github.com/BlueManCZ/hyprmod
Source0:        %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

# Extra sources for bundled wheels
Source1:        hyprland_config-0.9.16-py3-none-any.whl
Source2:        hyprland_monitors-0.9.0-py3-none-any.whl
Source3:        hyprland_schema-0.7.1-py3-none-any.whl
Source4:        hyprland_socket-0.12.2-py3-none-any.whl
Source5:        hyprland_state-0.4.7-py3-none-any.whl

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3dist(hatchling)
BuildRequires:  python3dist(installer)
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel

Requires:       gtk4
Requires:       libadwaita
Requires:       lua
Requires:       (hyprland or hyprland-git)

%description
HyprMod is a native GTK4/libadwaita settings application for Hyprland.

%prep
%autosetup

%build
%pyproject_wheel

%install
%pyproject_install

# Unpack bundled wheels into buildroot
for whl in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5}; do
    python3 -m installer --destdir="%{buildroot}" "$whl"
done

# Copy system metadata files to standard locations
install -Dpm0644 \
    %{buildroot}%{python3_sitelib}/hyprmod/data/applications/io.github.bluemancz.hyprmod.desktop \
    %{buildroot}%{_datadir}/applications/io.github.bluemancz.hyprmod.desktop

install -Dpm0644 \
    %{buildroot}%{python3_sitelib}/hyprmod/data/icons/hicolor/scalable/apps/io.github.bluemancz.hyprmod.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.github.bluemancz.hyprmod.svg

install -Dpm0644 \
    %{buildroot}%{python3_sitelib}/hyprmod/data/metainfo/io.github.bluemancz.hyprmod.metainfo.xml \
    %{buildroot}%{_metainfodir}/io.github.bluemancz.hyprmod.metainfo.xml

# Save files list ONLY for the primary hyprmod package and manage the wheels in files otherwise we builderror
%pyproject_save_files hyprmod

%files -f "%{pyproject_files}"
%license LICENSE
%doc README.md
%{_bindir}/hyprmod
%{_datadir}/applications/io.github.bluemancz.hyprmod.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.bluemancz.hyprmod.svg
%{_metainfodir}/io.github.bluemancz.hyprmod.metainfo.xml
%{python3_sitelib}/hyprland_*

%changelog
%autochangelog
