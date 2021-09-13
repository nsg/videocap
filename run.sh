#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $SCRIPT_DIR/$1

make_ramdisk() {
    sudo mkdir -p $RAMDISK
    sudo mount -t tmpfs -o size=64m tmpfs $RAMDISK
    sudo chown $USER $RAMDISK
}

recorder() {
    ffmpeg \
        -rtsp_transport tcp \
        -i rtsp://$RTSP_CAMERA_SOURCE \
        -reconnect 1 \
        -vcodec copy \
        -acodec copy \
        -map 0 \
        -f segment \
        -segment_time 10 \
        -segment_format mp4 \
        -segment_wrap 10 \
        -reset_timestamps 1 \
        "$RAMDISK/ffmpeg_capture-%01d.mp4"
}

analyzer() {
    local file="$1"

    echo "ANALYZE: $file"
    if ./analyze.py "$RAMDISK" "$file"; then
        echo "Found movement, push image"
        UNT="$(date +%s%N)"
        mv $RAMDISK/{match,$UNT}.jpg
        ./push-nextcloud.sh $RAMDISK/$UNT.jpg
    fi
}

watch_for_new_file() {
    inotifywait -qe close_write --format "%f" $RAMDISK
}

[ ! -d $RAMDISK ] && make_ramdisk

if [ "x$2" == xrecorder ]; then
    recorder
elif [ "x$2" == "xanalyzer" ]; then
    while true; do
        analyzer "$(watch_for_new_file)"
    done
fi
