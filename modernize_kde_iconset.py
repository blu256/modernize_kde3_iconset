#!/bin/env python3
#-*- coding: utf-8 -*-
#
# KDE3 Icon Theme Modernizer
#
# This script can convert a KDE3 icon theme to the XDG standard so that
# it becomes compatible with Trinity and other Desktop Enviroments.
#
# Copyright © 2021-22 Mavridis Philippe (aka blu.256)
#                               <mavridisf@gmail.com>
#
# Based on data from icon conversion scripts found on TGW:
#   http://mirror.git.trinitydesktop.org/gitea/TDE/scripts
#
#   (c) 2015 Timothy Pearson
#   All Rights Reserved
#

### IMPORTS
#
from os import path, rename, symlink

try:
    import configparser

except ImportError:
    print("Could not import module 'configparser'.")
    print("Your python3 installation must be really messed up.")
    exit(1)

### CONVERSION DATA
#
# Only these three icon types probably need to be updated
convert = {
    "Actions": {
        "previous":               "go-previous",
        "next":                   "go-next",
        "start":                  "go-first",
        "finish":                 "go-last",
        "stop":                   "process-stop",
        "lock":                   "system-lock-screen",
        "exit":                   "system-log-out",
        "run":                    "system-run",
        "up":                     "go-up",
        "down":                   "go-down",
        "top":                    "go-top",
        "bottom":                 "go-bottom",
        "undo":                   "edit-undo",
        "redo":                   "edit-redo",
        "find":                   "edit-find",
        "revert":                 "document-revert",
        "filenew":                "document-new",
        "fileopen":               "document-open",
        "fileprint":              "document-print",
        "filequickprint":         "document-print-preview",
        "filesave":               "document-save",
        "filesaveas":             "document-save-as",
        "fileclose":              "window-close",
        "editclear":              "edit-clear",
        "editcopy":               "edit-copy",
        "editcut":                "edit-cut",
        "editdelete":             "edit-delete",
        "editpaste":              "edit-paste",
        "folder_new":             "folder-new",
        "gohome":                 "go-home",
        "mail_forward":           "mail-forward",
        "mail_new":               "mail-message-new",
        "mail_replyall":          "mail-reply-all",
        "mail_reply":             "mail-reply-sender",
        "mail_send":              "mail-send",
        "player_pause":           "media-playback-pause",
        "player_stop":            "media-playback-stop",
        "player_rew":             "media-seek-backward",
        "player_fwd":             "media-seek-forward",
        "player_start":           "media-skip-backward",
        "player_end":             "media-skip-forward",
        "rotate_ccw":             "object-rotate-left",
        "rotate_cw":              "object-rotate-right",
        "window_fullscreen":      "view-fullscreen",
        "window_nofullscreen":    "view-restore",
        "window_new":             "window-new",
        "viewmagfit":             "zoom-fit-best",
        "viewmag+":               "zoom-in",
        "viewmag1":               "zoom-original",
        "viewmag-":               "zoom-out",
        "unindent":               "format-indent-less",
        "indent":                 "format-indent-more",
        "centrejust":             "format-justify-center",
        "leftjust":               "format-justify-left",
        "rightjust":              "format-justify-right",
        "text_left":              "format-text-direction-ltr",
        "text_right":             "format-text-direction-rtl",
        "text_bold":              "fotmat-text-bold",
        "text_italic":            "format-text-italic",
        "text_under":             "format-text-underline",
        "text_strike":            "format-text-strikethrough",
        "spellcheck":             "tools-check-spelling",
        "package_development":    "applications-development",
        "package_games":          "applications-games",
        "package_graphics":       "applications-graphics",
        "package_network":        "applications-internet",
        "package_multimedia":     "applications-multimedia",
        "package_wordprocessing": "applications-office",
        "edu_science":            "applications-science",
        "package_utilities":      "applications-utilities",
        "input_devices_settings": "preferences-desktop-peripherials",
        "kcmsystem":              "preferences-system",
        "personal":               "preferences-desktop-personal",
        "looknfeel":              "preferences-desktop"
    },

    "Devices": {
        "system":                        "computer",
        "hdd_unmount_encrypt":           "drive-harddisk-encrypted",
        "hdd_unmount_decrypt":           "drive-harddisk-decrypted",
        "hdd_mount_decrypt":             "drive-harddisk-decrypted-mounted",
        "hdd_unmount":                   "drive-harddisk",
        "hdd_mount":                     "drive-harddisk-mounted",
        "keyboard":                      "input-keyboard",
        "mouse":                         "input-mouse",
        "tablet":                        "input-tablet",
        "sd_mmc_unmount_encrypt":        "media-flash-sd_mmc-encrypted",
        "sd_mmc_unmount_decrypt":        "media-flash-sd_mmc-decrypted",
        "sd_mmc_mount_decrypt":          "media-flash-sd_mmc-decrypted-mounted",
        "sd_mmc_unmount":                "media-flash-sd_mmc",
        "sd_mmc_mount":                  "media-flash-sd_mmc-mounted",
        "usbpendrive_unmount_encrypt":   "media-flash-usb-encrypted",
        "usbpendrive_unmount_decrypt":   "media-flash-usb-decrypted",
        "usbpendrive_mount_decrypt":     "media-flash-usb-decrypted-mounted",
        "usbpendrive_unmount":           "media-flash-usb",
        "usbpendrive_mount":             "media-flash-usb-mounted",
        "smart_media_unmount_encrypt":   "media-flash-smart_media-encrypted",
        "smart_media_unmount_decrypt":   "media-flash-smart_media-decrypted",
        "smart_media_mount_decrypt":     "media-flash-smart_media-decrypted-mounted",
        "smart_media_unmount":           "media-flash-smart_media",
        "smart_media_mount":             "media-flash-smart_media-mounted",
        "memory_stick_unmount_encrypt":  "media-flash-memory_stick-encrypted",
        "memory_stick_unmount_decrypt":  "media-flash-memory_stick-decrypted",
        "memory_stick_mount_decrypt":    "media-flash-memory_stick-decrypted-mounted",
        "memory_stick_unmount":          "media-flash-memory_stick",
        "memory_stick_mount":            "media-flash-memory_stick-mounted",
        "compact_flash_unmount_encrypt": "media-flash-compact_flash-encrypted",
        "compact_flash_unmount_decrypt": "media-flash-compact_flash-decrypted",
        "compact_flash_mount_decrypt":   "media-flash-compact_flash-decrypted-mounted",
        "compact_flash_unmount":         "media-flash-compact_flash",
        "compact_flash_mount":           "media-flash-compact_flash-mounted",
        "3floppy_unmount":               "media-floppy-3_5",
        "3floppy_mount":                 "media-floppy-3_5-mounted",
        "5floppy_unmount":               "media-floppy-5_14",
        "5floppy_mount":                 "media-floppy-5_14-mounted",
        "zip_unmount":                   "media-floppy-zip",
        "cdrom_unmount_encrypt":         "media-optical-cdrom-encrypted",
        "cdrom_unmount_decrypt":         "media-optical-cdrom-decrypted",
        "cdrom_mount_decrypt":           "media-optical-cdrom-decrypted-mounted",
	    "cdrom_unmount":                 "media-optical-cdrom",
        "cdrom_mount":                   "media-optical-cdrom-mounted",
        "cdwriter_unmount_encrypt":      "media-optical-cdwriter-encrypted",
        "cdwriter_unmount_decrypt":      "media-optical-cdwriter-decrypted",
        "cdwriter_mount_decrypt":        "media-optical-cdwriter-decrypted-mounted",
        "cdwriter_unmount":              "media-optical-cdwriter",
        "cdwriter_mount":                "media-optical-cdwriter-mounted",
        "dvd_unmount_encrypt":           "media-optical-dvd-encrypted",
        "dvd_unmount_decrypt":           "media-optical-dvd-decrypted",
        "dvd_mount_decrypt":             "media-optical-dvd-decrypted-mounted",
        "dvd_unmount":                   "media-optical-dvd",
        "dvd_mount":                     "media-optical-dvd-mounted",
        "cdaudio_unmount":               "media-optical-cdaudio",
        "cdaudio_mount":                 "media-optical-cdaudio-mounted",
        "tape_unmount":                  "media-tape",
        "tape_mount":                    "media-tape-mounted",
        "ipod_unmount":                  "multimedia-player",
        "ipod_mount":                    "multimedia-player-mounted",
        "printer1":                      "printer"
    },

    "MimeTypes": {
        "sound":           "audio-x-generic",
        "font":            "font-x-generic",
        "image":           "image-x-generic",
        "html":            "text-html",
        "document":        "text-x-generic",
        "document2":       "text-x-generic-template",
        "shellscript":     "text-x-script",
        "video":           "video-x-generic",
        "vcard":           "x-office-address-book",
        "vcalendar":       "x-office-calendar",
        "kword_kwd":       "x-office-document",
        "applix":          "application-x-applix-word",
        "ascii":           "text-vnd.tde.ascii",
        "binary":          "application-octet-stream",
        "bt":              "application-x-bittorrent",
        "cdimage":         "application-x-cd-image",
        "cdr":             "application-x-cdr",
        "cdtrack":         "application-x-cda",
        "colorscm":        "application-x-kcsrc",
        "core":            "application-x-core",
        "database":        "application-vnd.oasis.opendocument.database",
        "deb":             "application-x-deb",
        "drawing":         "application-vnd.oasis.opendocument.graphics",
        "dvi":             "application-x-lyx",
        "empty":           "application-x-zerosize",
        "exec":            "application-x-executable",
        "exec_wine":       "application-x-mswinurl",
        "file_locked":     "application-vnd.tde.file.locked",
        "file_temporary":  "application-vnd.tde.file.temporary",
        "font_bitmap":     "application-x-font-snf",
        "font_truetype":   "application-x-font-ttf",
        "font_type1":      "application-x-font-type1",
        "gettext":         "application-x-gettext",
        "gf":              "application-x-tex-gf",
        "info":            "application-vnd.tde.info",
        "karbon_karbon":   "application-x-karbon",
        "kchart_chrt":     "application-x-kchart",
        "kexi_kexi":       "application-x-kexi",
        "kformula_kfo":    "application-x-kformula",
        "kivio_flw":       "application-x-kivio",
        "kpresenter_kpr":  "application-x-kpresenter",
        "krita_kra":       "application-x-krita",
     	"kspread_ksp":     "application-x-kspread",
    	"kugar_kud":       "application-x-kugar",
    	"log":             "text-x-log",
        "make":            "text-x-makefile",
        "man":             "application-x-troff-man",
        "metafont":        "application-x-metafont",
        "midi":            "audio-midi",
        "misc":            "application-vnd.tde.misc",
        "netscape_doc":    "application-x-netscape",
        "pdf":             "application-pdf",
        "pk":              "application-x-tex-pk",
        "postscript":      "application-postscript",
        "presentation":    "application-vnd.oasis.opendocument.presentation",
        "quicktime":       "video-x-quicktime",
        "readme":          "text-x-readme",
        "recycled":        "application-x-trash",
        "resource":        "application-vnd.tde.resource",
        "rpm":             "application-x-rpm",
        "rtf":             "text-rtf",
        "soffice":         "application-x-soffice",
        "source_c":        "text-x-csrc",
        "source_cpp":      "text-x-c++src",
        "source_f":        "text-x-fortran",
        "source_h":        "text-x-hsrc",
        "source_java":     "text-x-java",
        "source_j":        "text-x-jsrc",
        "source_l":        "text-x-lsrc",
        "source_moc":      "text-x-mocsrc",
        "source_o":        "text-x-osrc",
        "source_php":      "text-x-php",
        "source_pl":       "text-x-perl",
        "source":          "text-x-src",
        "source_p":        "text-x-psrc",
        "source_py":       "text-x-python",
        "source_s":        "text-x-asm",
        "source_y":        "text-x-ysrc",
        "spreadsheet":     "application-vnd.oasis.opendocument.spreadsheet",
        "tar":             "application-x-tar",
        "tdemultiple":     "application-vnd.tde.tdemultiple",
        "template_source": "application-vnd.tde.template_source",
        "tex":             "text-x-tex",
        "tgz":             "application-x-tarz",
        "txt2":            "application-vnd.tde.text.alt",
        "txt":             "text-plain",
        "vectorgfx":       "image-svg+xml",
        "widget_doc":      "application-x-designer",
        "wordprocessing":  "application-vnd.oasis.opendocument.text",
        "zip":             "application-vnd.tde.overlay.zip"
    }
}

# Directories array
directories = {}
for k in convert.keys():
    directories[k]=[]

### MAIN BODY
#
if __name__ == "__main__":
    print("KDE3 Iconset modernizer for Trinity")
    print("Copyright © 2021-2022 Mavridis Philippe (aka blu.256)")
    print()

    if not path.isfile("index.theme"):
        print("Error: This is not an iconset directory.")
        print("(It's missing the 'index.theme' file)")
        exit(2)

    # Parse theme file
    themefile = configparser.ConfigParser()
    themefile.read("index.theme")

    all_dirs = themefile["Icon Theme"]["Directories"]
    for d in all_dirs.split(","):
        type = themefile[d]["Context"]
        if type in directories.keys():
            directories[type].append(d)

    log = []
    for category in directories:
        for d in directories[category]:
            for f in convert[category]:
                print("[{}] {}\033[1000D\033[60C".format(d, f), end="")
                for ext in ('png','svg','svgz'):
                    src = path.join( d, f+"."+ext )
                    dst = path.join( d, convert[category][f]+"."+ext )

                    # Destination already exists, skip
                    if path.isfile(dst):
                        print("E" * len(ext), end="  ")
                        log.append( "E " + dst )

                    # Rename, if not a symlink
                    elif path.isfile(src) and not path.islink(src):
                        print(ext, end="  ")
                        rename(src, dst)
                        symlink(path.abspath(dst), src)
                        log.append( "R " + src.ljust(50) + " --> " + dst )

                    # Source is a link, report it
                    elif path.islink(src):
                        print("@" * len(ext), end="  ")
                        log.append( "@ " + src )

                    # File does not exist
                    else:
                        print("-" * len(ext), end="  ")

                print()
    logfile = open("conversion.log", "w")
    logfile.write( "\n".join(log) )
    logfile.close()
