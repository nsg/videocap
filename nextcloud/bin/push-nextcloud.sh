#!/bin/bash

# This script sends a file to a Nextcloud File Drop
# Token is the last path of the share URL

die() {
    echo "$@"
    exit 1
}

NEXTCLOUD_SERVER="$(snapctl get nextcloud-server)"
NEXTCLOUD_TOKEN="$(snapctl get nextcloud-token)"
NEXTCLOUD_PASSWORD=
FILE="$1"
URL="https://$NEXTCLOUD_SERVER/public.php/webdav"
FILEDEST="${FILE##*/}"

[ -z "$NEXTCLOUD_SERVER" ] && die 'You need to specify a Nextcloud URL server with "snap set videocap nextcloud-server=nextcloud.example.com"'
[ -z "$NEXTCLOUD_TOKEN" ] && die 'You need to specify a Nextcloud File Drop Token with "snap set videocap nextcloud-token=hUil..'
[ -z "$1" ] && die 'You need to specify a file to send'
[ ! -f "$1" ] && die 'File not found, please specify a full path to a single file'

curl -sT "$FILE" -u "$NEXTCLOUD_TOKEN":"$PASSWORD" -H "X-Requested-With: XMLHttpRequest" "$URL/$FILEDEST"
