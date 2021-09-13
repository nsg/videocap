#!/bin/bash

. config.sh

play() {
    ffplay -rtsp_transport tcp rtsp://192.168.3.106:554/s0
}

#ffplay -rtsp_transport tcp -vf fps=1 rtsp://192.168.3.106:554/s0

RAMDISK=/mnt/ramdisk

make_ramdisk() {
    sudo mkdir -p $RAMDISK
    sudo mount -t tmpfs -o size=64m tmpfs $RAMDISK
    sudo chown $USER $RAMDISK
}

recorder() {
    ffmpeg \
        -rtsp_transport tcp \
        -i rtsp://127.0.0.1:5554/s0 \
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

[ ! -d /mnt/ramdisk ] && make_ramdisk

if [ "x$1" == xrecorder ]; then
    recorder
elif [ "x$1" == "xanalyzer" ]; then
    while true; do
        analyzer "$(watch_for_new_file)"
    done
fi

#ffmpeg -rtsp_transport tcp -i "rtsp://..." -reconnect 1 \ 
#       -f segment -segment_format flv -segment_time 10 -segment_atclocktime 1 \ 
#       -reset_timestamps 1 -strftime 1 -avoid_negative_ts 1 \ 
#       -c copy -map 0 %Y%m%d-%H%M%S.flv
