%global ns_name ea-apache24
%global module_name mod_bwlimited

Summary: Provides cPanel's way of disabling bandwidth exceeders
Name: ea-apache24-mod_bwlimited
Version: 1.4
Release: 3%{?dist}
License: Unknown
Group: System Environment/Daemons
URL: http://cpanel.net/
Source0: mod_bwlimited-1.4.tar.gz
BuildRequires: ea-apache24-devel
Requires: ea-apache24-mmn = %{_httpd_mmn}
Requires(pre): ea-apache24

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
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.modules.d/
install -m 644 -p $RPM_SOURCE_DIR/490_bwlimited.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.modules.d/490_bwlimited.conf

%files
%defattr(0640,root,root,0755)
%attr(755,root,root)%{_httpd_moddir}/*.so
%config(noreplace) %{_sysconfdir}/apache2/conf.modules.d/490_bwlimited.conf

%changelog
* Thu Dec 24 2015 Dan Muey <dan@cpanel.net> - 1.4-3
- Enable module by installing 490_bwlimited.conf

* Thu May 28 2015 Julian Brown <julian.brown@cpanel.net> - 1.4-2
* Name changes for the rpm and required rpms. 

* Wed Nov 26 2014 Matt Dees <matt@cpanel.net> - 1.4-1
* Implement a new spec
