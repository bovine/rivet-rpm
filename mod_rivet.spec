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
	    --with-rivet-target-dir=%{_libdir}/httpd/rivet%{version}   \
            --disable-debug \
            --with-pic \
            --disable-rpath
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make
make doc

%check


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/httpd/modules/mod_rivet.la
rm -f $RPM_BUILD_ROOT%{_libdir}/httpd/rivet%{version}/librivet*.la


# Create an Apache conf include
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d
cat <<EOT >$RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/rivet.conf

# Loads the module.
LoadModule rivet_module modules/mod_rivet.so

# Let the module handle .rvt and .tcl files.
AddType application/x-httpd-rivet  rvt
AddType application/x-rivet-tcl    tcl

# The default charset can be specified in the configuration
AddType "application/x-httpd-rivet; charset=utf-8" rvt

# Add index.rvt to the list of files that will be served
DirectoryIndex index.rvt

EOT


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/httpd/modules/mod_rivet.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/rivet.conf

%dir %{_libdir}/httpd/rivet%{version}
%{_libdir}/httpd/rivet%{version}/README
%{_libdir}/httpd/rivet%{version}/init.tcl
%{_libdir}/httpd/rivet%{version}/pkgIndex.tcl
%attr(0755,root,root) %{_libdir}/httpd/rivet%{version}/librivet.so
%attr(0755,root,root) %{_libdir}/httpd/rivet%{version}/librivetparser.so
%dir %{_libdir}/httpd/rivet%{version}/packages
%{_libdir}/httpd/rivet%{version}/packages/README
%dir %{_libdir}/httpd/rivet%{version}/packages/commserver
%{_libdir}/httpd/rivet%{version}/packages/commserver/*.tcl
%dir %{_libdir}/httpd/rivet%{version}/packages/dio
%{_libdir}/httpd/rivet%{version}/packages/dio/*.tcl
%dir %{_libdir}/httpd/rivet%{version}/packages/dtcl
%{_libdir}/httpd/rivet%{version}/packages/dtcl/*.tcl
%dir %{_libdir}/httpd/rivet%{version}/packages/form
%{_libdir}/httpd/rivet%{version}/packages/form/form.tcl
%{_libdir}/httpd/rivet%{version}/packages/form/pkgIndex.tcl
%dir %{_libdir}/httpd/rivet%{version}/packages/rivet_ncgi
%{_libdir}/httpd/rivet%{version}/packages/rivet_ncgi/rivet_ncgi.tcl
%dir %{_libdir}/httpd/rivet%{version}/packages/session
%{_libdir}/httpd/rivet%{version}/packages/session/README.txt
%{_libdir}/httpd/rivet%{version}/packages/session/*.tcl
%{_libdir}/httpd/rivet%{version}/packages/session/*.sql
%{_libdir}/httpd/rivet%{version}/packages/session/session-demo.rvt
%{_libdir}/httpd/rivet%{version}/packages/session/session-httpd.conf
%dir %{_libdir}/httpd/rivet%{version}/packages/simpledb
%{_libdir}/httpd/rivet%{version}/packages/simpledb/pkgIndex.tcl
%{_libdir}/httpd/rivet%{version}/packages/simpledb/simpledb.tcl
%{_libdir}/httpd/rivet%{version}/packages/simpledb/simpledb.test
%dir %{_libdir}/httpd/rivet%{version}/packages/tclrivet
%{_libdir}/httpd/rivet%{version}/packages/tclrivet/README
%{_libdir}/httpd/rivet%{version}/packages/tclrivet/parse.tcl
%{_libdir}/httpd/rivet%{version}/packages/tclrivet/pkgIndex.tcl
%{_libdir}/httpd/rivet%{version}/packages/tclrivet/tclrivet.tcl
%{_libdir}/httpd/rivet%{version}/packages/tclrivet/tclrivetparser.tcl
%dir %{_libdir}/httpd/rivet%{version}/rivet-tcl
%{_libdir}/httpd/rivet%{version}/rivet-tcl/README
%{_libdir}/httpd/rivet%{version}/rivet-tcl/*.tcl
%{_libdir}/httpd/rivet%{version}/rivet-tcl/tclIndex

%doc LICENSE NOTICE contrib doc/html doc/examples

%changelog
* Wed Apr 14 2010 Jeff Lawson <jeff@bovine.net> 0.8.0-20100414032008
- Initial creation of rpm spec

