%global ns_name ea-apache24
%global module_name mod_bwlimited

Summary: Provides cPanel's way of disabling bandwidth exceeders
Name: ea-apache24-mod_bwlimited
Version: 1.4
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4556 for more details
%define release_prefix 47
Release: %{release_prefix}%{?dist}.cpanel
License: Unknown
Group: System Environment/Daemons
URL: http://cpanel.net/
Vendor: cPanel, Inc.
Source0: mod_bwlimited-1.4.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
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
install %{module_name}.so %{buildroot}%{_httpd_moddir}/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.modules.d/
install -p $RPM_SOURCE_DIR/490_bwlimited.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.modules.d/490_mod_bwlimited.conf

%clean
rm -rf %{buildroot}

%files
%defattr(0640,root,root,0755)
%attr(755,root,root)%{_httpd_moddir}/*.so
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/apache2/conf.modules.d/490_mod_bwlimited.conf

%changelog
* Wed May 20 2020 Julian Brown <julian.brown@cpanel.net> - 1.4-47
- ZC-6836: Build on CentOS 8

* Fri Dec 16 2016 Jacob Perkins <jacob.perkins@cpanel.net> - 1.4-46
- EA-5493: Added vendor field

* Mon Jun 20 2016 Dan Muey <dan@cpanel.net> - 1.4-45
- EA-4383: Update Release value to OBS-proof versioning

* Tue Jan 05 2016 S. Kurt Newman <kurt.newman@cpanel.net> - 1.4-4
- Change bwlimited.conf to 0644 so that normal users can load modules
  the same as Apache while testing their configuration with 'httpd -t'
- Also renamed configuration to 490_mod_bwlimited.conf to match the
  naming scheme of our other files.

* Thu Dec 24 2015 Dan Muey <dan@cpanel.net> - 1.4-3
- Enable module by installing 490_bwlimited.conf

* Thu May 28 2015 Julian Brown <julian.brown@cpanel.net> - 1.4-2
* Name changes for the rpm and required rpms.

* Wed Nov 26 2014 Matt Dees <matt@cpanel.net> - 1.4-1
* Implement a new spec
