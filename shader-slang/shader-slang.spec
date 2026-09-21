%global upstream_name slang
%global github_owner  shader-slang
%global debug_package %{nil}

Name:           shader-slang
Version:        2026.18
Release:        %autorelease
Summary:        Shading language that makes it easier to build and maintain large shader codebases

License:        Apache-2.0 WITH LLVM-exception
URL:            https://github.com/%{github_owner}/%{upstream_name}
Source0:        %{upstream_name}-%{version}-full.tar.gz

Patch:          fedora.patch

BuildRequires:  cmake
BuildRequires:  curl
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  mesa-libGL-devel
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  unzip
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools-devel
BuildRequires:  vulkan-headers
BuildRequires:  miniz-devel
BuildRequires:  glslang-devel

%description
Slang is a shading language that makes it easier to build and maintain large shader codebases in a modular and extensible fashion, while also maintaining the highest possible performance on modern GPUs and graphics APIs. Slang is based on years of collaboration between researchers at NVIDIA, Carnegie Mellon University, Stanford, MIT, UCSD and the University of Washington.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development headers and CMake modules for integrating Slang into C/C++ applications.

%prep
%autosetup -n slang-%{version} -p1

%build
%cmake \
    -GNinja \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DSLANG_VERSION_NUMERIC=%{version} \
    -DSLANG_VERSION_FULL=%{version} \
    -DSLANG_ENABLE_OPTIX=OFF \
    -DSLANG_RHI_ENABLE_OPTIX=OFF \
    -DSLANG_ENABLE_CUDA=OFF \
    -DSLANG_ENABLE_DXIL=OFF \
    -DSLANG_ENABLE_SLANG_RHI=OFF \
    -DSLANG_ENABLE_TESTS=OFF \
    -DSLANG_ENABLE_EXAMPLES=OFF \
    -DSLANG_ENABLE_GFX=OFF \
    -DSLANG_ENABLE_SLANGD=OFF \
    -DSLANG_ENABLE_REPLAYER=OFF \
    -DSLANG_SLANG_LLVM_FLAVOR=DISABLE \
    -DSLANG_USE_SYSTEM_MINIZ=ON \
    -DSLANG_USE_SYSTEM_VULKAN_HEADERS=ON \
    -DSLANG_USE_SYSTEM_SPIRV_HEADERS=ON \
    -DSLANG_USE_SYSTEM_SPIRV_TOOLS=ON \
    -DSLANG_USE_SYSTEM_GLSLANG=ON

%cmake_build

# Stage libraries and all .slang core modules expected in Release/ by cmake_install
mkdir -p %{_vpath_builddir}/Release/lib %{_vpath_builddir}/Release/bin
find %{_vpath_builddir} -name "libslang-llvm.so" -exec cp -f {} %{_vpath_builddir}/Release/lib/ \; 2>/dev/null || true
find . -name "*.slang" -not -path "*/Release/*" -exec cp -f {} %{_vpath_builddir}/Release/bin/ \; 2>/dev/null || true

%install
%cmake_install

# Relocate all installed contents from /usr/lib to /usr/lib64 on 64-bit systems
if [ "%{_lib}" = "lib64" ] && [ -d "%{buildroot}%{_prefix}/lib" ]; then
    mkdir -p %{buildroot}%{_libdir}
    cp -av %{buildroot}%{_prefix}/lib/* %{buildroot}%{_libdir}/
    rm -rf %{buildroot}%{_prefix}/lib
fi

# Remove auto-installed internal test files and generated docs
rm -rf %{buildroot}%{_datadir}/doc

%files
%license LICENSE
%doc README.md
%{_bindir}/*
%{_libdir}/libslang*.so.*
%{_libdir}/slang-standard-module-%{version}/

%files devel
%{_includedir}/slang*.h
%{_libdir}/cmake/slang/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libslang*.so

%changelog
%autochangelog
