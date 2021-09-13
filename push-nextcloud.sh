#!/bin/bash

# Send files to a File Drop 
# Usage:
# NEXTCLOUD_SERVER=... TOKEN=... ./push-nextcloud.sh /my/file
#
# token is the last path of the share URL

FILE="$1"
PASSWORD=
URL="https://$NEXTCLOUD_SERVER/public.php/webdav"
FILEDEST="${FILE##*/}"

curl -T "$FILE" -u "$NEXTCLOUD_TOKEN":"$PASSWORD" -H "X-Requested-With: XMLHttpRequest" "$URL/$FILEDEST"
