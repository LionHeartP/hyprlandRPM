%global commit0 473804b3594dd829295484f1f479a560b8114f2d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global bumpver 1517

%global __provides_exclude_from ^(%{_libdir}/hyprland/.*\\.so)$

%global plugins %{shrink:
                csgo-vulkan-fix
                hyprbars
                hyprexpo
                hyprfocus
}

%if !%{defined build_for}
%global build_for git
%endif

%define pluginsmeta %{lua:
if rpm.expand("%build_for") == "git" then
    rpm.define("pluginssuffix -git")
    rpm.define(rpm.expand("pluginsmetaname hyprland-plugins%pluginssuffix"))
    rpm.define(rpm.expand("hyprlandpkg hyprland%pluginssuffix"))
else
    rpm.define("pluginsmetaname hyprland-plugins")
    rpm.define("hyprlandpkg hyprland")
end
}

%pluginsmeta

Name:           %{pluginsmetaname}
Version:        0.1^%{bumpver}.git%{shortcommit0}
Release:        %autorelease
Summary:        Official plugins for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-plugins
Source:         %{url}/archive/%{commit0}/%{name}-%{commit0}.tar.gz

#Hyprexpo fix
Patch:          https://github.com/hyprwm/hyprland-plugins/pull/650.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  %{hyprlandpkg}-devel

Requires:       %{hyprlandpkg} = %_hyprland_version

# print Recommends: for each plugin
%{lua:for w in rpm.expand('%plugins'):gmatch("%S+") do print("Recommends: hyprland-plugin-"..w..(rpm.expand("%build_for") == "git" and "-git" or "")..'\n') end}

%description
%{summary}.

%define _package() \%package -n hyprland-plugin-%1%{?pluginssuffix:%{pluginssuffix}}\
Summary:       %1 plugin for %{hyprlandpkg}\
Requires:      %{hyprlandpkg} = %_hyprland_version\
\%description  -n hyprland-plugin-%1%{?pluginssuffix:%{pluginssuffix}}\
\%1 plugin for %{hyprlandpkg}.\
\%files -n     hyprland-plugin-%1%{?pluginssuffix:%{pluginssuffix}}\
\%%license LICENSE\
\%dir %{_libdir}/hyprland\
\%{_libdir}/hyprland/lib%1.so\

# expand %%_package for each plugin
%{lua:for w in rpm.expand('%plugins'):gmatch("%S+") do print(rpm.expand("%_package "..w)..'\n\n') end}


%prep
%autosetup -n hyprland-plugins-%{commit0} -p1
# Hyprfocus temp fix
sed -i 's/\bm_activeInactiveAlpha\b/m_alpha/g' hyprfocus/main.cpp
sed -i 's/m_alpha\[0\]/m_alpha[(Desktop::View::eWindowAlpha)0]/g' hyprfocus/main.cpp
sed -i 's/m_alpha->/m_alpha[(Desktop::View::eWindowAlpha)0]->/g' hyprfocus/main.cpp
sed -i 's/\*window->m_alpha/(*window->m_alpha[(Desktop::View::eWindowAlpha)0])/g' hyprfocus/main.cpp
sed -i 's/\*w->m_alpha/(*w->m_alpha[(Desktop::View::eWindowAlpha)0])/g' hyprfocus/main.cpp

%build
for plugin in %{plugins}
do
pushd $plugin
%cmake -DCMAKE_INSTALL_LIBDIR=%{_libdir}/hyprland
%cmake_build
popd
done


%install
for plugin in %{plugins}
do
pushd $plugin
%cmake_install
popd
done


%files


%changelog
%autochangelog
