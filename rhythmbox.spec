%define _disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define	gstapi	1.0
%define major 	8
%define gimajor	3.0
%define libname %mklibname rhythmbox %{major}
%define girname	%mklibname %{name}-gir %{gimajor}

Summary:	Music Management Application 
Name:		rhythmbox
Version:	3.0.2
Release:	3
License:	GPLv2+ with exception
Group:		Sound
Url:		http://www.gnome.org/projects/rhythmbox/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/rhythmbox/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	vala
BuildRequires:	python3-devel
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	pkgconfig(clutter-1.0) >= 1.2
BuildRequires:	pkgconfig(clutter-gst-2.0) >= 1.0
BuildRequires:	pkgconfig(clutter-gtk-1.0) >= 1.0
BuildRequires:	pkgconfig(clutter-x11-1.0) >= 1.2
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(grilo-0.2) >= 0.1.17
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
BuildRequires:	pkgconfig(mx-1.0) >= 1.0.1
BuildRequires:	pkgconfig(pygobject-3.0) >= 2.90.2
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(totem-plparser)
BuildRequires:	pkgconfig(webkitgtk-3.0)

Suggests:	grilo-plugins
Suggests:	media-player-info

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
Requires:	typelib(WebKit)
Requires:	python3-gi
#Zeitgeist has not been ported to python3 so its plugin doesnt work
#Requires:	typelib(Zeitgeist)
#Requires:	zeitgeist
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

%package mozilla
Group:		Sound
Summary:	Rhythmbox integration for Mozilla Firefox
Requires:	%{name} = %{version}

%description mozilla
This plugin integates Rhythmbox with Mozilla and compatible
browsers. It provides a handler for itms:// Links to Apples iTunes
Music Store.

%package devel
Group:		Development/C
Summary:	Rhythmbox plugin development files
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description devel
Install this if you want to build Rhythmbox plugins.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--disable-gtk-doc \
	--with-libsecret \
	--enable-vala

%make 

%install
%makeinstall_std _ENABLE_SK=false
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
%{_iconsdir}/hicolor/*/apps/rhythmbox*
#% {_iconsdir}/hicolor/*/places/music-library.*
%{_iconsdir}/hicolor/*/status/rhythmbox-*
%{_libexecdir}/rhythmbox-metadata
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/artsearch
%{_libdir}/%{name}/plugins/audiocd
%{_libdir}/%{name}/plugins/audioscrobbler
%{_libdir}/%{name}/plugins/context
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
#{_libdir}/%{name}/plugins/rbzeitgeist
%{_libdir}/%{name}/plugins/replaygain
%{_libdir}/%{name}/plugins/sendto
%{_libdir}/%{name}/sample-plugins
%{_libdir}/%{name}/plugins/visualizer
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/librhythmbox-core.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/MPID-%{gimajor}.typelib
%{_libdir}/girepository-1.0/RB-%{gimajor}.typelib

%files mozilla
%{_libdir}/mozilla/plugins/librhythmbox-itms-detection-plugin.so

%files devel
%{_includedir}/%{name}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gtk-doc/html/%{name}
%{_datadir}/gir-1.0/MPID-%{gimajor}.gir
%{_datadir}/gir-1.0/RB-%{gimajor}.gir


%changelog
* Wed Apr 23 2014 Crispin Boylan <crisb@mandriva.org> 3.0.2-3
+ Revision: 0f24b1f
- Requires webkit typelib

* Tue Apr 22 2014 Crispin Boylan <crisb@mandriva.org> 3.0.2-2
+ Revision: 6501ff1
- Fix

* Tue Apr 22 2014 Crispin Boylan <crisb@mandriva.org> 3.0.2-2
+ Revision: 76f4414
- Remove zeitgeist plugin due to no python3 version

* Tue Apr 22 2014 Crispin Boylan <crisb@mandriva.org> 3.0.2-1
+ Revision: 065d970
- Fix BR

* Tue Apr 22 2014 Crispin Boylan <crisb@mandriva.org> 3.0.2-1
+ Revision: 14962da
- Fix BR

* Mon Apr 21 2014 Crispin Boylan <crisb@mandriva.org> 3.0.2-1
+ Revision: b09ae45
- 3.0.2, fix requires on plugins

* Tue Apr 15 2014 Crispin Boylan <crisb@mandriva.org> 3.0.1-1
+ Revision: 945cc72
- Fix file list

* Tue Apr 15 2014 Crispin Boylan <crisb@mandriva.org> 3.0.1-1
+ Revision: e971cc0
- Fix file list

* Fri Mar 07 2014 Crispin Boylan <crisb@mandriva.org> 3.0.1-1
+ Revision: a533d0d
- Brasero in contrib

* Fri Mar 07 2014 Crispin Boylan <crisb@mandriva.org> 3.0.1-1
+ Revision: ac9e885
- Brasero in contrib

* Tue Mar 04 2014 Crispin Boylan <crisb@mandriva.org> 3.0.1-1
+ Revision: bc772f8
- 3.0.1

* Tue Mar 04 2014 Crispin Boylan <crisb@mandriva.org> 3.0.1-1
+ Revision: 931fcef
- 3.0.1

* Tue Mar 04 2014 Crispin Boylan <crisb@mandriva.org> 3.0-1
+ Revision: 3dc7ce9
- 3.0

* Sat Feb 08 2014 Tomasz Paweł Gajc <tpgxyz@gmail.com> 2.99.1-2
+ Revision: dbe1b88
- MassBuild#328: Increase release tag

* Sat Dec 07 2013 Bernhard Rosenkraenzer <bero@bero.eu> 3.0-5
+ Revision: 0774f34
- MassBuild#289: Increase release tag

* Sat Dec 07 2013 Bernhard Rosenkraenzer <bero@bero.eu> 3.0-4
+ Revision: 377a7ed
- MassBuild#289: Increase release tag

* Sat Dec 07 2013 Bernhard Rosenkraenzer <bero@bero.eu> 3.0-3
+ Revision: 382beeb
- MassBuild#289: Increase release tag

* Sat Dec 07 2013 Bernhard Rosenkraenzer <bero@bero.eu> 3.0-2
+ Revision: 282aa31
- MassBuild#289: Increase release tag

* Sat Sep 14 2013 Alexander Khryukin <alexander@mezon.ru> 3.0-1
+ Revision: 720e11a
- BR python-devel replaced with python3-devel

* Fri Sep 13 2013 Alexander Khryukin <alexander@mezon.ru> 3.0-1
+ Revision: 457cb1e
- br python

* Fri Sep 13 2013 Alexander Khryukin <alexander@mezon.ru> 3.0-1
+ Revision: d4f510b
- version update 3.0

* Fri Jul 05 2013 mdawkins (Matthew Dawkins) <mattydaw@gmail.com> 2.99.1-1
+ Revision: 0b1b5de
- adjusted reqs

* Fri Jul 05 2013 mdawkins (Matthew Dawkins) <mattydaw@gmail.com> 2.99.1-1
+ Revision: 829bf2c
- new version 2.99.1
- cleaned up specs

* Sun Mar 31 2013 Crispin Boylan <crisb@mandriva.org> 2.98-1
+ Revision: 8e24a3c
- Fix file list

* Sat Mar 30 2013 Crispin Boylan <crisb@mandriva.org> 2.98-1
+ Revision: db0f3c9
- disable visualizer again

* Sat Mar 30 2013 Crispin Boylan <crisb@mandriva.org> 2.98-1
+ Revision: 5dace84
- 2.98

* Sat Mar 30 2013 Crispin Boylan <crisb@mandriva.org> 2.97-4
+ Revision: 5f54b72
- Disable some stuff for now

* Sat Mar 30 2013 Crispin Boylan <crisb@mandriva.org> 2.97-4
+ Revision: 0fdfe60
- Allow undefined

* Sat Mar 30 2013 Crispin Boylan <crisb@mandriva.org> 2.97-4
+ Revision: f16525c
- Disable patch

* Sat Mar 30 2013 Crispin Boylan <crisb@mandriva.org> 2.97-4
+ Revision: b8f2c17
- Fix BR

* Sat Mar 30 2013 Crispin Boylan <crisb@mandriva.org> 2.97-4
+ Revision: 53e877a
- Fix BR

* Fri Feb 08 2013 Jochen Schoenfelder <arisel@arisel.de> 2.97-3
+ Revision: de8b544
- New build

* Wed Jan 30 2013 Bernhard Rosenkränzer <bero@lindev.ch> 2.97-2
+ Revision: b59dd21
- Fix .abf.yml syntax

* Sun Jun 03 2012 goetz <goetz@mandriva.org> 2.97-2
+ Revision: 4ca91e3
- fix build dep for musicbrainz
- SILENT: svn-revision: 802173


