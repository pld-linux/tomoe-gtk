#
# Conditional build:
%bcond_without	gucharmap	# gucharmap support
%bcond_without	python		# build without python bindings
%bcond_without	static_libs	# don't build static libraries
#
%define		tomoe_ver	0.6.0
Summary:	GTK library for tomoe for Japanese and Chinese handwritten input
Summary(pl.UTF-8):	Biblioteka GTK dla tomoe do wprowadzania japońskiego i chińskiego pisma ręcznego
Name:		tomoe-gtk
Version:	0.6.0
Release:	3
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/tomoe/%{name}-%{version}.tar.gz
# Source0-md5:	bd49ac64549d8a7ab092bea1c1dc04fc
Patch0:		%{name}-rpath.patch
Patch1:		%{name}-cflags.patch
Patch2:		%{name}-gucharmap.patch
URL:		http://scim-imengine.sourceforge.jp/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	gtk-doc >= 1.4
BuildRequires:	gtk+2-devel >= 2:2.4.0
%{?with_gucharmap:BuildRequires:	gucharmap2-devel >= 1.4.0}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	tomoe-devel >= %{tomoe_ver}
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-pygobject-devel
BuildRequires:	python-pygtk-devel >= 2:2.0
BuildRequires:	python-tomoe-devel
%endif
Requires:	gtk+2 >= 2:2.4.0
%{?with_gucharmap:Requires:	gucharmap2 >= 1.4.0}
Requires:	tomoe >= %{tomoe_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GTK library for tomoe Japanese and Chinese handwritten input. This
package is used by scim-tomoe or uim-tomoe.

%description -l pl.UTF-8
Biblioteka GTK do tomoe - systemu wprowadzania ręcznego pisma
japońskiego i chińskiego. Ten pakiet jest wykorzystywany przez
scim-tomoe oraz uim-tomoe.

%package devel
Summary:	Header files for GTK tomoe library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GTK tomoe
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2-devel >= 2:2.4.0
%{?with_gucharmap:Requires:	gucharmap2-devel >= 1.4.0}
Requires:	tomoe-devel >= %{tomoe_ver}

%description devel
The libtomoe-devel package includes the header files for libtomoe-gtk.
Install this if you want to develop programs which will use
libtomoe-gtk.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki libtomoe-gtk. Należy go
zainstalować, aby tworzyć programy wykorzystujące tę bibliotekę.

%package static
Summary:	Tomoe-GTK static library
Summary(pl.UTF-8):	Biblioteka statyczna Tomoe-GTK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Tomoe-GTK static library.

%description static -l pl.UTF-8
Biblioteka statyczna Tomoe-GTK.

%package -n python-tomoe-gtk
Summary:	Tomoe-GTK bindings for Python
Summary(pl.UTF-8):	Wiązania Tomoe-GTK dla Pythona
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-tomoe-gtk
Tomoe-GTK bindings for Python.

%description -n python-tomoe-gtk -l pl.UTF-8
Wiązania Tomoe-GTK dla Pythona.

%prep
%setup -q
%patch -P0 -p0
%patch -P1 -p0
%patch -P2 -p1

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-rpath \
	%{!?with_gucharmap:--without-gucharmap} \
	--with-html-dir=%{_gtkdocdir}

%{__make} \
	RPM_CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%if %{with python}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/gtk-2.0/tomoegtk.{a,la}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libtomoe-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtomoe-gtk.so.0
%{_datadir}/tomoe-gtk

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtomoe-gtk.so
%{_includedir}/tomoe/gtk
%{_pkgconfigdir}/tomoe-gtk.pc
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
