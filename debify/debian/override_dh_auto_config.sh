#!/bin/bash

source debian/vars.sh

$_httpd_apxs -c mod_bwlimited.c
mv .libs/$module_name.so .
strip -g $module_name.so
