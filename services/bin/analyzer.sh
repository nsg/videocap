#!/bin/bash

if [[ "$(snapctl get analyzer)" != "enabled" ]] && [[ "$ANALYZER" != "enabled" ]]; then
    echo "Analytics service not enabled, shutting down service"
    snapctl stop videocap.analyzer-service
    exit 0
fi

RAMDISK=/var/videocap

analyzer() {
    local file="$1"

    echo "ANALYZE: $file"
    if $SNAP/bin/analyzer "$file"; then
        echo "Found movement in $file, push image"
        UNT="$(date +%s%N)"
        mv $RAMDISK/{match,$UNT}.jpg
        $SNAP/bin/push-nextcloud.sh $RAMDISK/$UNT.jpg && rm $RAMDISK/$UNT.jpg

        # Save the last nine files that triggers movement for debug
        cp "$RAMDISK/$file" $SNAP_COMMON
    fi
}

watch_for_new_file() {
    inotifywait -qe close_write --format "%f" $RAMDISK
}

while true; do
    analyzer "$(watch_for_new_file)"
done
