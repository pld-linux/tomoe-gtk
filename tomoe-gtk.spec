#
# Conditional build:
%bcond_without	python		# build without python bindings
%bcond_without	static_libs	# don't build static libraries
#
%define		tomoe_ver	0.6.0
Summary:	Gtk library for tomoe for Japanese and Chinese handwritten input
Name:		tomoe-gtk
Version:	%{tomoe_ver}
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/tomoe/%{name}-%{version}.tar.gz
# Source0-md5:	bd49ac64549d8a7ab092bea1c1dc04fc
Patch0:		%{name}-rpath.patch
Patch1:		%{name}-cflags.patch
URL:		http://scim-imengine.sourceforge.jp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	tomoe-devel >= %{tomoe_ver}
BuildRequires:	gtk+2-devel
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-tomoe
BuildRequires:	python-pygobject-devel
BuildRequires:	python-pygtk-devel
%endif
Requires:	tomoe >= %{tomoe_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gtk library for tomoe Japanese handwritten input. This package is used
by scim-tomoe or uim-tomoe.

%package devel
Summary:	Gtk library for tomoe Japanese handwritten input
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2-devel
Requires:	tomoe-devel

%description devel
The libtomoe-devel package includes the header files for libtomoe-gtk.
Install this if you want to develop programs which will use
libtomoe-gtk.

%package static
Summary:	Tomoe-GTK static library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Tomoe-GTK static library.

%package -n python-tomoe-gtk
Summary:	Tomoe-GTK bindings for python
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-tomoe-gtk
Tomoe-GTK bindings for python.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__automake}
%configure \
	--without-gucharmap \
	--disable-rpath \
	--with-html-dir=%{_gtkdocdir}

%{__make} RPM_CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{py_sitedir}/gtk-2.0/tomoegtk.{a,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README TODO
%attr(755,root,root) %{_libdir}/libtomoe-gtk.so.*.*.*
%attr(755,root,root) %{_libdir}/libtomoe-gtk.so.[0-9]
%{_datadir}/tomoe-gtk

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/tomoe-gtk.pc
%{_libdir}/libtomoe-gtk.so
%{_includedir}/tomoe/gtk
%{_gtkdocdir}/libtomoe-gtk

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtomoe-gtk.a
%endif

%if %{with python}
%files -n python-tomoe-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/gtk-2.0/tomoegtk.so
%endif
