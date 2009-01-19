%define version 0.11.6
%define svn r6131
%define release %mkrel 5.%svn.1

%define		gstreamer 0.10.0
%define		gstname gstreamer0.10

%define major 0
%define libname %mklibname rhythmbox %major

Name:		rhythmbox
Summary:	Music Management Application 
Version:	%version
Release:	%release
License:	GPLv2+ with exception
Group:		Sound
Source:		http://ftp.gnome.org/pub/GNOME/sources/rhythmbox/%{name}-%{svn}.tar.bz2
# gw take default Internet radio station listing from Fedora:
Source1: http://cvs.fedoraproject.org/viewcvs/*checkout*/rpms/rhythmbox/devel/rhythmbox-iradio-initial.pls
# gw remove invalid file name characters for VFAT on iPods
# https://bugzilla.redhat.com/show_bug.cgi?id=440668
Patch5: rhythmbox-0.11.5-ipod-vfat.patch
#gw: add more radio stations
Patch6: rhythmbox-more-radios.patch

URL:		http://www.gnome.org/projects/rhythmbox/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires:  libgnomeui2-devel
BuildRequires:  libglade2.0-devel
BuildRequires:  libid3tag-devel
BuildRequires:  libmusicbrainz-devel
BuildRequires:  libmusicbrainz3-devel
BuildRequires:  libvorbis-devel
BuildRequires:  perl-XML-Parser
BuildRequires:  libgpod-devel
BuildRequires:  libflac-devel
BuildRequires:  scrollkeeper
BuildRequires: libsoup-devel
BuildRequires: libsexy-devel
BuildRequires: libxrender-devel
BuildRequires: gstreamer0.10-python-devel
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
BuildRequires:  libmtp-devel >= 0.3.0
BuildRequires:  gnome-media libcddb-slave2-devel
BuildRequires:  libvala-devel
BuildRequires:  xulrunner-devel
BuildRequires:  gtk-doc
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	gnome-doc-utils
Requires: %gstname-plugins-base
Requires: %gstname-plugins-good
Requires: %gstname-plugins-ugly
Requires:	%gstname-gnomevfs >= %gstreamer
Requires:	%gstname-flac >= %gstreamer
Requires:	dbus-x11
Requires: gstreamer0.10-python
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

%package mozilla
Group: Sound
Summary: Rhythmbox integration for Mozilla Firefox
Requires: %name = %version

%description mozilla
This plugin integates Rhythmbox with Mozilla and compatible
browsers. It provides a handler for itms:// Links to Apples iTunes
Music Store.

%package upnp
Group: Sound
Summary: Rhythmbox UPNP plugin
Requires: %name = %version-%release
Requires: python-coherence

%description upnp
This plugin adds UPNP support to Rhythmbox. It allows playing media
from, and sending media to UPnP/DLNA network devices.

%prep
%setup -q -n %name
cp %SOURCE1 .
%patch5 -p0 -b .ipod-vfat
%patch6 -p0
./autogen.sh
%build
#gw rb.c
%define Werror_cflags %nil
#gw else librhythmbox-core does not build
%define _disable_ld_no_undefined 1
%configure2_5x \
--enable-nautilus-menu --enable-ipod --enable-ipod-writing --enable-daap --enable-tag-writing \
--enable-vala \
--with-mdns=avahi \
--enable-gtk-doc \
--with-gnome-keyring
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


rm -f  %buildroot%_libdir/%name/plugins/*/*.a \
   %buildroot%_libdir/%name/plugins/*.a \
   %buildroot%_libdir/*.a \
   %buildroot%_libdir/mozilla/plugins/lib*a
#gw remove it until there's a devel package
rm -f  %buildroot%_libdir/librhythmbox-core.{so,la}

find %buildroot -name \*.la |xargs chmod 644

# Replace the default radios with Ogg Radios
cp -a rhythmbox-iradio-initial.pls %{buildroot}%{_libdir}/rhythmbox/plugins/iradio/iradio-initial.pls


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

%if %mdkversion < 200900
%post
%update_menus
%post_install_gconf_schemas rhythmbox
%update_scrollkeeper
%update_icon_cache hicolor

%postun
%{clean_menus}
%clean_scrollkeeper
%clean_icon_cache hicolor

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig
%endif

%preun
%preun_uninstall_gconf_schemas rhythmbox

%files -f %name.lang
%defattr(-, root, root)
%doc AUTHORS COPYING README NEWS
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
%dir %_libdir/%name/
%dir %_libdir/%name/plugins
%_libdir/%name/plugins/artdisplay
%_libdir/%name/plugins/audiocd
%_libdir/%name/plugins/audioscrobbler
%_libdir/%name/plugins/cd-recorder
%_libdir/%name/plugins/daap
%_libdir/%name/plugins/dontreallyclose
%_libdir/%name/plugins/fmradio
%_libdir/%name/plugins/generic-player
%_libdir/%name/plugins/ipod
%_libdir/%name/plugins/iradio
%_libdir/%name/plugins/jamendo
%_libdir/%name/plugins/*sample-vala*
%_libdir/%name/plugins/lyrics
%_libdir/%name/plugins/magnatune
%_libdir/%name/plugins/mmkeys
%_libdir/%name/plugins/mtpdevice
%_libdir/%name/plugins/power-manager
%_libdir/%name/plugins/python-console
%_libdir/%name/plugins/rb
%_libdir/%name/plugins/rblirc
%_libdir/%name/plugins/visualizer

%files upnp
%defattr(-, root, root)
%_libdir/%name/plugins/upnp_coherence

%files -n %libname
%defattr(-, root, root)
%_libdir/librhythmbox-core.so.%{major}*

%files mozilla
%defattr(-, root, root)
%_libdir/mozilla/plugins/librhythmbox-itms-detection-plugin.so
