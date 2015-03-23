%global ns_name ea
%global module_name mod_bwlimited

Summary: Provides cPanel's way of disabling bandwidth exceeders
Name: %{ns_name}-%{module_name}
Version: 1.4
Release: 1%{?dist}
License: Unknown
Group: System Environment/Daemons
URL: http://cpanel.net/
Source0: mod_bwlimited-1.4.tar.gz
BuildRequires: ea-apache2-devel
Requires: ea-apache2-mmn = %{_httpd_mmn}
Requires(pre): ea-apache2

# Suppres auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_libdir}/httpd/modules/.*\.so$}
%{?filter_setup}

%description
This module is used for tracking and disabling bandwidth when a user exceed their
bandwidth allocation

%prep
%setup -n %{module_name}-%{version}

%build
%{_httpd_apxs} -c mod_bwlimited.c
mv .libs/%{module_name}.so .
%{__strip} -g %{module_name}.so

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_httpd_moddir}
install -m755 %{module_name}.so %{buildroot}%{_httpd_moddir}/

%files
%defattr(0640,root,root,0755)
%attr(755,root,root)%{_httpd_moddir}/*.so


%changelog
* Wed Nov 26 2014 Matt Dees <matt@cpanel.net> - 1.4-1
* Implement a new spec
