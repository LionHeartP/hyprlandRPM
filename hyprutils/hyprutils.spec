Name:           hyprutils
Version:        0.13.1
Release:        %autorelease -b2
Summary:        Hyprland utilities library used across the ecosystem

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprutils
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Backport commits so we don't crash hyprland-git
Patch:          https://github.com/hyprwm/hyprutils/commit/3cd3972b2ee658a14d2610d8494e09259e530124.patch
Patch:          https://github.com/hyprwm/hyprutils/commit/40ede2e7bdec80ba5d4c443160d905e9f841ae5f.patch
Patch:          https://github.com/hyprwm/hyprutils/commit/9157e1c70f2126849768c49ec3c280ff548e4379.patch
Patch:          https://github.com/hyprwm/hyprutils/commit/9d8bf6e810597152eef8906c670b96679af2faec.patch
Patch:          https://github.com/hyprwm/hyprutils/commit/d2b40ffe7bfcb001bbf5888bb56ff646de53e7db.patch
Patch:          https://github.com/hyprwm/hyprutils/commit/65876d972857d55677076fb8d70e098728ba03e0.patch
Patch:          https://github.com/hyprwm/hyprutils/commit/476b8566de057166d3a0dc2b00a102988d193247.patch
Patch:          https://github.com/hyprwm/hyprutils/commit/41fb809557abd29a57151b6e1aaeabd05f9437e1.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:	gtest-devel

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Development files for %{name}.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.%{version}
%{_libdir}/lib%{name}.so.12

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
%autochangelog
