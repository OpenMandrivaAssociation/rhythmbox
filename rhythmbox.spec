#gw rb.c
%define Werror_cflags %nil

%define	gstname gstreamer0.10

%define major 3
%define libname %mklibname rhythmbox %{major}

Name:		rhythmbox
Summary:	Music Management Application 
Version:	2.96
Release:	1
License:	GPLv2+ with exception
Group:		Sound
URL:		http://www.gnome.org/projects/rhythmbox/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/rhythmbox/%{name}-%{version}.tar.xz
%endif
# gw take default Internet radio station listing from Fedora:
Source1: http://cvs.fedoraproject.org/viewcvs/*checkout*/rpms/rhythmbox/devel/rhythmbox-iradio-initial.pls
#gw: add more radio stations
Patch6: rhythmbox-more-radios.patch

BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	vala
BuildRequires:	libdmapsharing-devel
BuildRequires:	lirc-devel
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	pkgconfig(clutter-1.0) >= 1.2
BuildRequires:	pkgconfig(clutter-gst-1.0) >= 1.0
BuildRequires:	pkgconfig(clutter-gtk-1.0) >= 1.0
BuildRequires:	pkgconfig(clutter-x11-1.0) >= 1.2
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(grilo-0.1) >= 0.1.17
BuildRequires:	pkgconfig(gstreamer-0.10) >= 0.10.32
BuildRequires:	pkgconfig(gstreamer-interfaces-0.10) >= 0.10.32
BuildRequires:	pkgconfig(gstreamer-pbutils-0.10) >= 0.10.32
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10) >= 0.10.32
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.2.0
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libbrasero-media3)
BuildRequires:	pkgconfig(libgpod-1.0)
BuildRequires:	pkgconfig(libmtp)
BuildRequires:	pkgconfig(libmusicbrainz3)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpeas-1.0) >= 0.7.3
BuildRequires:	pkgconfig(libpeas-gtk-1.0) >= 0.7.3
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libsoup-gnome-2.4)
BuildRequires:	pkgconfig(mx-1.0) >= 1.0.1
BuildRequires:	pkgconfig(pygobject-3.0) >= 2.90.2
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(totem-plparser)
BuildRequires:	pkgconfig(webkitgtk-3.0)

# For python plugins
Requires:	python-gobject
Suggests:	media-player-info

Requires:	dbus-x11
Requires:	%{gstname}-plugins-base
Requires:	%{gstname}-plugins-good
Suggests:	%{gstname}-plugins-ugly
Requires:	%{gstname}-gnomevfs
Requires:	%{gstname}-flac
#Suggests 	%{gstname}-faad
Requires(post,postun):	GConf2

%description
Music Management application with support for ripping audio-cd's,
playback of Ogg Vorbis and Mp3 and burning of CD-Rs.

%package -n %{libname}
Group:System/Libraries
Summary: Shared library part of %{name}

%description -n %{libname}
Music Management application with support for ripping audio-cd's,
playback of Ogg Vorbis and Mp3 and burning of CD-Rs.

This is the shared library part of %{name}.

%package mozilla
Group: Sound
Summary: Rhythmbox integration for Mozilla Firefox
Requires: %{name} = %{version}

%description mozilla
This plugin integates Rhythmbox with Mozilla and compatible
browsers. It provides a handler for itms:// Links to Apples iTunes
Music Store.

%package upnp
Group: Sound
Summary: Rhythmbox UPNP plugin
Requires: %{name} = %{version}-%{release}
Requires: python-coherence
Requires: python-louie

%description upnp
This plugin adds UPNP support to Rhythmbox. It allows playing media
from, and sending media to UPnP/DLNA network devices.

%package devel
Group: Development/C
Summary: Rhythmbox plugin development files
Requires: %{libname} = %{version}-%{release}

%description devel
Install this if you want to build Rhythmbox plugins.

%prep
%setup -q
cp %SOURCE1 .
%patch6 -p0

%build
%configure2_5x \
	--disable-static \
	--disable-scrollkeeper \
	--with-mdns=avahi \
	--enable-gtk-doc \
	--enable-vala \
	--with-gnome-keyring

%make 

%install
%makeinstall_std _ENABLE_SK=false
find %{buildroot} -type f -name "*.la" -delete -print
%find_lang %{name} --with-gnome

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="Audio;Player" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

# Replace the default radios with Ogg Radios
cp -a rhythmbox-iradio-initial.pls %{buildroot}%{_libdir}/rhythmbox/plugins/iradio/iradio-initial.pls

# save space by linking identical images in translated docs
helpdir=%{buildroot}%{_datadir}/gnome/help/%{name}
for f in $helpdir/C/figures/*.png; do
  b="$(basename $f)"
  for d in $helpdir/*; do
    if [ -d "$d" -a "$d" != "$helpdir/C" ]; then
      g="$d/figures/$b"
      if [ -f "$g" ]; then
        if cmp -s $f $g; then
          rm "$g"; ln -s "../../C/figures/$b" "$g"
        fi
      fi
    fi
  done
done

%check
# gw one test fails without a running dbus
#xvfb-run make check

%files -f %{name}.lang
%doc AUTHORS COPYING README NEWS
%{_bindir}/rhythmbox
%{_bindir}/rhythmbox-client
%{_datadir}/applications/rhythmbox.desktop
%{_datadir}/applications/rhythmbox-device.desktop
%{_datadir}/icons/hicolor/*/apps/rhythmbox*
%{_datadir}/icons/hicolor/*/places/music-library.*
%{_datadir}/rhythmbox/
%{_datadir}/gtk-doc/html/%{name}
%{_datadir}/dbus-1/services/org.gnome.Rhythmbox.service
%{_libexecdir}/rhythmbox-metadata
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/artdisplay
%{_libdir}/%{name}/plugins/audiocd
%{_libdir}/%{name}/plugins/audioscrobbler
%{_libdir}/%{name}/plugins/cd-recorder
%{_libdir}/%{name}/plugins/context
%{_libdir}/%{name}/plugins/daap
%{_libdir}/%{name}/plugins/dbus-media-server
%{_libdir}/%{name}/plugins/fmradio
%{_libdir}/%{name}/plugins/generic-player
%{_libdir}/%{name}/plugins/im-status
%{_libdir}/%{name}/plugins/ipod
%{_libdir}/%{name}/plugins/iradio
%{_libdir}/%{name}/plugins/jamendo
%{_libdir}/%{name}/plugins/lyrics
%{_libdir}/%{name}/plugins/magnatune
%{_libdir}/%{name}/plugins/mmkeys
%{_libdir}/%{name}/plugins/mpris
%{_libdir}/%{name}/plugins/mtpdevice
%{_libdir}/%{name}/plugins/power-manager
%{_libdir}/%{name}/plugins/python-console
%{_libdir}/%{name}/plugins/rb
%{_libdir}/%{name}/plugins/rblirc
%{_libdir}/%{name}/plugins/rbzeitgeist
%{_libdir}/%{name}/plugins/replaygain
%{_libdir}/%{name}/plugins/sample-vala
%{_libdir}/%{name}/plugins/sendto
%{_libdir}/%{name}/plugins/status-icon
%{_libdir}/%{name}/plugins/visualizer
%{_mandir}/man1/*.1*

%files upnp
%{_libdir}/%{name}/plugins/upnp_coherence

%files -n %{libname}
%{_libdir}/librhythmbox-core.so.%{major}*

%files mozilla
%{_libdir}/mozilla/plugins/librhythmbox-itms-detection-plugin.so

%files devel
%{_includedir}/%{name}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc

