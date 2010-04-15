%define contentdir /var/www
%define rivet_snapshot 20100414032008
%define debug_package %{nil} 

Summary: Apache Rivet lets you use the Tcl scripting language to create dynamic web sites
Name: mod_rivet
Version: 0.8.0
Release: %{rivet_snapshot}
License: Apache License Version 2.0
Group: Development/Languages
URL: http://tcl.apache.org/rivet/

Source0: http://cvs.apache.org/snapshots/tcl-rivet/tcl-rivet_%{rivet_snapshot}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: httpd-devel >= 2.0.46-1
BuildRequires: gcc-c++, libstdc++-devel
BuildRequires: tcl >= 8.5, tcl-devel >= 8.5
BuildRequires: autoconf >= 2.59, automake >= 1.9, libtool >= 1.4.3
Provides: mod_rivet = %{version}-%{release}
Requires: httpd
Requires: tcl >= 8.5

%description
Tcl is a scripting language.  Apache Rivet is a module for Apache
httpd that makes it easy easy for developers to write dynamically
generated webpages in Tcl.

%prep
%setup -q -n tcl-rivet


%build

aclocal
autoreconf

%configure --with-tcl=%{_libdir}/tcl8.5/       \
            --with-apxs=%{_sbindir}/apxs       \
            --with-tclsh=%{_bindir}/tclsh8.5   \
	    --with-apache=%{_prefix}           \
            --with-apache-version=2            \
            --disable-debug \
            --with-pic \
            --disable-rpath
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make

%check


%install
#[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# start with an empty rivet-tcl directory
make uninstall-local

# actually install
make install

# Install the default configuration file and icons
#install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
#install -m 644 $RPM_SOURCE_DIR/php.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
#install -m 755 -d $RPM_BUILD_ROOT%{contentdir}/icons
#install -m 644    *.gif $RPM_BUILD_ROOT%{contentdir}/icons/

# install the DSO
#install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules
#install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# install the ZTS DSO
#install -m 755 build-zts/libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/libphp5-zts.so

# Apache config fragment
#install -m 755 -d $RPM_BUILD_ROOT/etc/httpd/conf.d
#install -m 644 $RPM_SOURCE_DIR/php.conf $RPM_BUILD_ROOT/etc/httpd/conf.d

#install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
#install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
#install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session


# Remove unpackaged files
#rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
#       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
#       $RPM_BUILD_ROOT%{_datadir}/pear \
#       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

rm -f %{_libdir}/httpd/modules/mod_rivet.la

# Remove irrelevant docs
#rm -f README.{Zeus,QNX,CVS-RULES}


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_rivet.so
%dir %{_libdir}/rivet%{version}
%attr(0755,root,root) %{_libdir}/rivet%{version}/librivet*.so

#%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
#%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
#%config(noreplace) %{_sysconfdir}/httpd/conf.d/php.conf
#%{contentdir}/icons/php.gif

#%files common -f files.common
#%defattr(-,root,root)
#%doc Zend/ZEND_* TSRM_LICENSE regex_COPYRIGHT
#%config(noreplace) %{_sysconfdir}/php.ini
#%dir %{_sysconfdir}/php.d
#%dir %{_libdir}/php
#%dir %{_libdir}/php/modules
#%dir %{_localstatedir}/lib/php
#%dir %{_libdir}/php/pear
#%dir %{_datadir}/php


%changelog
* Wed Apr 14 2010 Jeff Lawson <jeff@bovine.net> 0.8.0-20100414032008
- Initial creation of rpm spec

