#!/bin/bash

source debian/vars.sh

set -x

rm -rf $DEB_INSTALL_ROOT
mkdir -p $DEB_INSTALL_ROOT$_httpd_moddir
install $module_name.so $DEB_INSTALL_ROOT$_httpd_moddir/
mkdir -p $DEB_INSTALL_ROOT$_sysconfdir/apache2/conf.modules.d/
install -p $SOURCE8001 $DEB_INSTALL_ROOT$_sysconfdir/apache2/conf.modules.d/490_mod_bwlimited.conf
