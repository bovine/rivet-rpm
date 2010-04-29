%define debug_package %{nil} 

Summary: Apache Rivet lets you use the Tcl scripting language to create dynamic web sites
Name: mod_rivet
Version: 2.0.0
Release: 1%{?dist}
License: Apache License Version 2.0
Group: Development/Languages
URL: http://tcl.apache.org/rivet/

Source0: http://www.apache.org/dist/tcl/rivet/rivet-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: httpd-devel >= 2.0.46-1
BuildRequires: gcc-c++
BuildRequires: libstdc++-devel
BuildRequires: tcl >= 8.5
BuildRequires: tcl-devel >= 8.5
BuildRequires: autoconf >= 2.59
BuildRequires: automake >= 1.9
BuildRequires: libtool >= 1.4.3

Provides: mod_rivet = %{version}-%{release}

Requires: httpd
Requires: tcl >= 8.5

%description
Tcl is a scripting language.  Apache Rivet is a module for Apache
httpd that makes it easy easy for developers to write dynamically
generated webpages in Tcl.

%prep
%setup -q -n rivet-%{version}


%build

%{__aclocal}
autoreconf -vfs

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

%{__make} %{?_smp_mflags} 
%{__make} %{?_smp_mflags} doc


%install

%{__make} install DESTDIR=%{buildroot}

# Remove static libraries
rm -f %{buildroot}%{_libdir}/httpd/modules/mod_rivet.la
rm -f %{buildroot}%{_libdir}/httpd/rivet%{version}/librivet*.la

# Create an Apache conf include
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d
cat <<EOT >%{buildroot}/%{_sysconfdir}/httpd/conf.d/rivet.conf

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
%{__rm} -rf %{buildroot} 


%files
%defattr(-, root, root, 0755)
%doc LICENSE NOTICE contrib doc/html doc/examples
%config(noreplace) %{_sysconfdir}/httpd/conf.d/rivet.conf
%{_libdir}/httpd/modules/mod_rivet.so
%{_libdir}/httpd/rivet%{version}


%changelog
* Thu Apr 29 2010 Jeff Lawson <jeff@bovine.net> 2.0.0
- Update for new release.

* Wed Apr 14 2010 Jeff Lawson <jeff@bovine.net> 0.8.0-20100414032008
- Initial creation of rpm spec

