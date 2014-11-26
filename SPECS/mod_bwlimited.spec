%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Summary: mod_bwlimited
Name: mod_bwlimited
Version: 1.4
Release: 1%{?dist}
License: Unknown
Group: System Environment/Daemons
URL: http://cpanel.net/
Source0: mod_bwlimited-1.4.tar.gz
BuildRequires: httpd-devel
Requires: httpd-mmn = %{_httpd_mmn}
Requires(pre): httpd

# Suppres auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_libdir}/httpd/modules/.*\.so$}
%{?filter_setup}

%description
This module is for doing authy stuff

%prep
%setup -n %{name}-%{version}

%build
%{_httpd_apxs} -c -i mod_bwlimited.c

%install
install -Dp -m 0644 .libs/mod_bwlimited.so $RPM_BUILD_ROOT%{_httpd_moddir}/mod_bwlimited.so

%files
%{_httpd_moddir}/*.so

%changelog
* Wed Nov 26 2014 Matt Dees <matt@cpanel.net> - 1.4-1
* implement spec
