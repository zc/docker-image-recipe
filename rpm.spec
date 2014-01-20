Name: dockerimage
Version: 0.3.0
Release: 1

Summary: %{name}
Group: Applications/ZC
Requires: cleanpython27 = 2.7.5
Requires: registry = 0.1
BuildRequires: cleanpython27
%define python /opt/cleanpython27/bin/python

##########################################################################
# Lines below this point normally shouldn't change

%define source %{name}-%{version}

Vendor: Zope Corporation
Packager: Zope Corporation <sales@zope.com>
License: ZPL
AutoReqProv: no
Source: %{source}.tgz
Prefix: /opt
BuildRoot: /tmp/%{name}

%description
%{summary}

%prep
%setup -n %{source}

%build
rm -rf %{buildroot}
mkdir %{buildroot} %{buildroot}/opt
cp -r $RPM_BUILD_DIR/%{source} %{buildroot}/opt/%{name}
%{python} %{buildroot}/opt/%{name}/install.py bootstrap
%{python} %{buildroot}/opt/%{name}/install.py buildout:extensions=
%{python} -m compileall -q -f -d /opt/%{name}/eggs  \
   %{buildroot}/opt/%{name}/eggs \
   > /dev/null 2>&1 || true
rm -rf %{buildroot}/opt/%{name}/release-distributions

# Gaaaa! buildout doesn't handle relative paths in egg links. :(
echo ../src > %{buildroot}/opt/%{name}/develop-eggs/zc.%{name}.egg-link 

%clean
rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{source}

%pre
rm -rf /opt/%{name}/eggs/setuptools*

%files
%defattr(-, root, root)
/opt/%{name}
