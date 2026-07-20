Name:           noctalia-hyprland-meta
Version:        0.2
Release:        7%{?dist}
Summary:        Meta-package to kickstart noctalia-shell on Hyprland
BuildArch:      noarch

License:        MIT

Source0:        hyprland.lua

Requires:       (hyprland or hyprland-git)
Requires:       hyprland-guiutils
Requires:       (noctalia or noctalia-git)

%description
A meta-package that installs hyprland and noctalia-shell. It provides a 
base hyprland configuration in /etc/skel to ensure noctalia-shell is 
automatically executed on first run for new users.

%prep

%build

%install
mkdir -p %{buildroot}/etc/skel/.config/hypr
install -pm 0644 %{SOURCE0} %{buildroot}/etc/skel/.config/hypr/

%post
if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
    USER_CONF="$USER_HOME/.config/hypr/hyprland.lua"
    if [ ! -f "$USER_CONF" ]; then
        mkdir -p "$(dirname "$USER_CONF")"
        cp /etc/skel/.config/hypr/hyprland.lua "$USER_CONF"
        chown -R "$SUDO_USER:" "$(dirname "$USER_CONF")"
    fi
fi

%files
%dir /etc/skel/.config/hypr
/etc/skel/.config/hypr/hyprland.lua

%changelog
* Sun Jul 05 2026 LionHeartP <LionHeartP@proton.me> - 0.2-6
- Allow git snapshots or stable for noctalia and hyprland 

* Wed Jul 01 2026 LionHeartP <LionHeartP@proton.me> - 0.2-4
- Update lua config

* Mon Jun 08 2026 LionHeartP <LionHeartP@proton.me> - 0.2-2
- Fix typo on lua config

* Mon Jun 08 2026 LionHeartP <LionHeartP@proton.me> - 0.2-1
- Migrate to noctalia v5 and hyprland lua config

* Sun Mar 29 2026 LionHeartP <LionHeartP@proton.me> - 0.1-1
- Initial release
