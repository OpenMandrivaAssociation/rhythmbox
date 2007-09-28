%define version 0.11.2

%define release %mkrel 2

%define		gstreamer 0.10.0
%define		gstname gstreamer0.10

%define major 0
%define libname %mklibname rhythmbox %major

Name:		rhythmbox
Summary:	Music Management Application 
Version:	%version
Release:	%release
License:	GPL
Group:		Sound
Source:		http://ftp.gnome.org/pub/GNOME/sources/rhythmbox/%{name}-%{version}.tar.bz2
#gw from Fedora, enable Magnatune and Jamendo by default
Patch1: rhythmbox-enable-stores.patch
URL:		http://www.rhythmbox.org
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires:  libgnomeui2-devel
BuildRequires:  libglade2.0-devel
BuildRequires:  libid3tag-devel
BuildRequires:  libmusicbrainz-devel
BuildRequires:  libvorbis-devel
BuildRequires:  perl-XML-Parser
BuildRequires:  libgpod-devel
BuildRequires:  libflac-devel
BuildRequires:  scrollkeeper
BuildRequires: libsoup-devel
BuildRequires: libsexy-devel
BuildRequires: libxrender-devel
BuildRequires: pygtk2.0-devel
BuildRequires: liblirc-devel
BuildRequires: desktop-file-utils
BuildRequires: libcheck-devel
BuildRequires: avahi-client-devel
BuildRequires: avahi-glib-devel
BuildRequires:  libnotify-devel >= 0.3.2
BuildRequires:  libgstreamer-plugins-base-devel >= %gstreamer
BuildRequires:  x11-server-xvfb
BuildRequires:  libnautilus-burn-devel > 2.11.3
BuildRequires:  libtotem-plparser-devel >= 1.1.3
BuildRequires:  libmtp-devel
BuildRequires:  gnome-media libcddb-slave2-devel
BuildRequires:  libvala-devel
BuildRequires:  gtk-doc
#BuildRequires:	automake1.8 gnome-common
BuildRequires:	intltool
BuildRequires:	gnome-doc-utils
Requires: %gstname-plugins-base
Requires: %gstname-plugins-good
Requires: %gstname-plugins-ugly
Requires:	%gstname-gnomevfs >= %gstreamer
Requires:	%gstname-flac >= %gstreamer
Requires:	dbus-x11
Requires: pygtk2.0-libglade
Requires: gnome-python
Requires: gnome-python-gconf
Requires: gnome-python-gnomevfs
#Suggests:	%gstname-faad
Provides:	net-rhythmbox
Obsoletes:	net-rhythmbox
Provides:	rhythmbox0.7
Obsoletes:	rhythmbox0.7
Provides:	rhythmbox-scrobbler
Obsoletes:	rhythmbox-scrobbler
Requires(post):		scrollkeeper
Requires(postun):	scrollkeeper
Requires(post):		GConf2 >= 2.3.3
Requires(preun):	GConf2 >= 2.3.3

%description
Music Management application with support for ripping audio-cd's,
playback of Ogg Vorbis and Mp3 and burning of CD-Rs.

%package -n %libname
Group:System/Libraries
Summary: Shared library part of %name

%description -n %libname
Music Management application with support for ripping audio-cd's,
playback of Ogg Vorbis and Mp3 and burning of CD-Rs.

This is the shared library part of %name.

%prep
%setup -q
cd data
%patch1
cd -

%build
%configure2_5x \
--enable-nautilus-menu --enable-ipod --enable-ipod-writing --enable-daap --enable-tag-writing \
--with-mdns=avahi \
--enable-gtk-doc
%make 

%install
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std _ENABLE_SK=false

%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/*/*{-??.omf,-??_??.omf};do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name.lang
done

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Audio;Player" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


rm -f  %buildroot%_libdir/%name/plugins/*.a %buildroot%_libdir/*.a
#gw remove it until there's a devel package
rm -f  %buildroot%_libdir/librhythmbox-core.{so,la}


find %buildroot -name \*.la |xargs chmod 644

%check
#gw I couldn't make the tests run in the iurt chroot
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%{_bindir}/Xvfb :$XDISPLAY &
export DISPLAY=:$XDISPLAY
# gw one test fails without a running dbus
#make check
kill $(cat /tmp/.X$XDISPLAY-lock) || :

%clean
rm -rf %{buildroot}

%post
%update_menus
%post_install_gconf_schemas rhythmbox
%update_scrollkeeper
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas rhythmbox

%postun
%{clean_menus}
%clean_scrollkeeper
%clean_icon_cache hicolor

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -f %name.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README NEWS
%config(noreplace) %{_sysconfdir}/gconf/schemas/rhythmbox.schemas
%{_bindir}/rhythmbox
%{_bindir}/rhythmbox-client
%{_datadir}/applications/rhythmbox.desktop
%{_datadir}/icons/hicolor/*/apps/rhythmbox*
%{_datadir}/rhythmbox/
%dir %_datadir/omf/rhythmbox/
%_datadir/omf/rhythmbox/rhythmbox-C.omf
%_datadir/gtk-doc/html/%name
%_datadir/dbus-1/services/org.gnome.Rhythmbox.service
%_libexecdir/rhythmbox-metadata
%_libdir/%name/

%files -n %libname
%defattr(-, root, root)
%_libdir/librhythmbox-core.so.%{major}*
