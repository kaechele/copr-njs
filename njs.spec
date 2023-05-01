%global _nginx_modsrcdir ../nginx

Name:           njs
Version:        0.7.12
Release:        %autorelease
Summary:        Scripting language for nginx

License:        BSD
URL:            https://nginx.org/en/docs/njs
Source0:        https://hg.nginx.org/njs/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-njs-remove-Werror-in-upstream-build-scripts.patch

BuildRequires:  gcc
BuildRequires:  nginx-mod-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  zlib-devel


%description
njs is a subset of the JavaScript language that allows extending nginx
functionality. njs is created in compliance with ECMAScript 5.1 (strict mode)
with some ECMAScript 6 and later extensions. The compliance is still evolving.


%package -n nginx-mod-http-js
Summary:    NJS module for nginx HTTP server

%description -n nginx-mod-http-js
Module that extends nginx' http functionalities with NJS scripting capabilities.


%package -n nginx-mod-stream-js
Summary:    NJS module for nginx stream server

%description -n nginx-mod-stream-js
Module that extends nginx' stream functionalities with NJS scripting
capabilities.


%prep
%autosetup -p1


%build
%nginx_modconfigure --with-stream
%nginx_modbuild
# njs doesn't use autotools
./configure \
    --cc-opt="%{optflags} $(pcre2-config --cflags)" \
    --ld-opt="$RPM_LD_FLAGS"
%make_build njs


%install
pushd %{_vpath_builddir}
install -dm 0755 %{buildroot}%{nginx_moddir}
install -pm 0755 ngx_{http,stream}_js_module.so %{buildroot}%{nginx_moddir}
install -dm 0755 %{buildroot}%{nginx_modconfdir}
echo 'load_module "%{nginx_moddir}/ngx_http_js_module.so";' \
    > %{buildroot}%{nginx_modconfdir}/mod-http-js.conf
echo 'load_module "%{nginx_moddir}/ngx_stream_js_module.so";' \
    > %{buildroot}%{nginx_modconfdir}/mod-stream-js.conf
popd
install -Dpm 0755 build/njs %{buildroot}/%{_bindir}/njs

%files
%license LICENSE
%doc CHANGES README
%{_bindir}/njs


%files -n nginx-mod-http-js
%license LICENSE
%doc CHANGES README
%{nginx_moddir}/ngx_http_js_module.so
%{nginx_modconfdir}/mod-http-js.conf


%files -n nginx-mod-stream-js
%license LICENSE
%doc CHANGES README
%{nginx_moddir}/ngx_stream_js_module.so
%{nginx_modconfdir}/mod-stream-js.conf


%changelog
%autochangelog

