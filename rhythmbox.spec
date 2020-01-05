%define _disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define	gstapi	1.0
%define major 	10
%define gimajor	3.0
%define libname %mklibname rhythmbox %{major}
%define girname	%mklibname %{name}-gir %{gimajor}

Summary:	Music Management Application 
Name:		rhythmbox
Version:	3.4.4
Release:	1
License:	GPLv2+ with exception
Group:		Sound
Url:		http://www.gnome.org/projects/rhythmbox/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/rhythmbox/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	vala
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	pkgconfig(clutter-1.0) >= 1.2
BuildRequires:	pkgconfig(clutter-gst-2.0) >= 1.0
BuildRequires:	pkgconfig(clutter-gtk-1.0) >= 1.0
BuildRequires:	pkgconfig(clutter-x11-1.0) >= 1.2
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(grilo-0.3)
BuildRequires:	pkgconfig(gstreamer-%{gstapi}) >= 0.10.32
BuildRequires:	pkgconfig(gstreamer-pbutils-%{gstapi}) >= 0.10.32
BuildRequires:	pkgconfig(gstreamer-plugins-base-%{gstapi}) >= 0.10.32
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.2.0
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libdmapsharing-3.0)
BuildRequires:	pkgconfig(libgpod-1.0)
BuildRequires:	pkgconfig(liblircclient0)
BuildRequires:	pkgconfig(libmtp)
BuildRequires:	pkgconfig(libdiscid)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpeas-1.0) >= 0.7.3
BuildRequires:	pkgconfig(libpeas-gtk-1.0) >= 0.7.3
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libsoup-gnome-2.4)
BuildRequires:	pkgconfig(pygobject-3.0) >= 2.90.2
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(totem-plparser)
#BuildRequires:	pkgconfig(libbrasero-media3)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.18.0
BuildRequires:	pkgconfig(gio-2.0) >= 2.26.0
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.26.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.32.0
BuildRequires:	yelp-tools
BuildRequires:	gettext-devel
BuildRequires:	python-gobject3

Recommends:	grilo-plugins
Recommends:	media-player-info

Requires:	dbus-x11
Requires:	gstreamer%{gstapi}-plugins-base
Requires:	gstreamer%{gstapi}-plugins-good
Suggests:	gstreamer%{gstapi}-plugins-ugly
Requires:	gstreamer%{gstapi}-flac
Requires:	gstreamer%{gstapi}-soup
# For python plugins
Requires:	python-gi
Requires:	typelib(Peas)
Requires:	typelib(PeasGtk)
#Requires:	typelib(WebKit)
Requires:	typelib(RB)
Requires:	typelib(MPID)
Requires:	python3-mako

# md no more upnp plugin
Obsoletes:	rhythmbox-upnp < 2.96

%description
Music Management application with support for ripping audio-cd's,
playback of Ogg Vorbis and Mp3 and burning of CD-Rs.

%package -n %{libname}
Group:System/Libraries
Summary:	Shared library part of %{name}

%description -n %{libname}
This is the shared library part of %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

#package mozilla
#Group:		Sound
#Summary:	Rhythmbox integration for Mozilla Firefox
#Requires:	%{name} = %{version}-%{release}

#description mozilla
#This plugin integates Rhythmbox with Mozilla and compatible
#browsers. It provides a handler for itms:// Links to Apples iTunes
#Music Store.

%package devel
Group:		Development/C
Summary:	Rhythmbox plugin development files
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description devel
Install this if you want to build Rhythmbox plugins.

%prep
%setup -q
%autosetup -p1

%build
%configure \
	--disable-gtk-doc \
	--with-libsecret \
	--without-webkit \
	--enable-vala

%make_build

%install
%make_install _ENABLE_SK=false
%find_lang %{name} --with-gnome

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="Audio;Player" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

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

# Remove the zeitgeist plugin as zeitgeist has not been ported to python3
rm -rf %{buildroot}%{_libdir}/%{name}/plugins/rbzeitgeist

%files -f %{name}.lang
%doc AUTHORS COPYING README NEWS
%{_bindir}/rhythmbox
%{_bindir}/rhythmbox-client
%{_datadir}/applications/rhythmbox.desktop
%{_datadir}/applications/rhythmbox-device.desktop
%{_datadir}/dbus-1/services/org.gnome.Rhythmbox3.service
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/rhythmbox/
%{_datadir}/metainfo/%{name}.appdata.xml
#{_iconsdir}/hicolor/*/apps/rhythmbox*
#% {_iconsdir}/hicolor/*/places/music-library.*
#{_iconsdir}/hicolor/*/status/rhythmbox-*
%{_libexecdir}/rhythmbox-metadata
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/android
%{_libdir}/%{name}/plugins/artsearch
%{_libdir}/%{name}/plugins/audiocd
%{_libdir}/%{name}/plugins/audioscrobbler
%{_libdir}/%{name}/plugins/context
%{_libdir}/%{name}/plugins/daap
%{_libdir}/%{name}/plugins/dbus-media-server
%{_libdir}/%{name}/plugins/fmradio
%{_libdir}/%{name}/plugins/generic-player
%{_libdir}/%{name}/plugins/grilo
%{_libdir}/%{name}/plugins/im-status
%{_libdir}/%{name}/plugins/ipod
%{_libdir}/%{name}/plugins/iradio
%{_libdir}/%{name}/plugins/lyrics
%{_libdir}/%{name}/plugins/magnatune
%{_libdir}/%{name}/plugins/mmkeys
%{_libdir}/%{name}/plugins/mpris
%{_libdir}/%{name}/plugins/mtpdevice
%{_libdir}/%{name}/plugins/notification
%{_libdir}/%{name}/plugins/power-manager
%{_libdir}/%{name}/plugins/python-console
%{_libdir}/%{name}/plugins/rb
%{_libdir}/%{name}/plugins/rblirc
%{_libdir}/%{name}/plugins/replaygain
%{_libdir}/%{name}/plugins/soundcloud
%{_libdir}/%{name}/plugins/webremote
%{_libdir}/%{name}/sample-plugins
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/librhythmbox-core.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/MPID-%{gimajor}.typelib
%{_libdir}/girepository-1.0/RB-%{gimajor}.typelib

#files mozilla
#{_libdir}/mozilla/plugins/librhythmbox-itms-detection-plugin.so

%files devel
%{_includedir}/%{name}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gtk-doc/html/%{name}
%{_datadir}/gir-1.0/MPID-%{gimajor}.gir
%{_datadir}/gir-1.0/RB-%{gimajor}.gir

