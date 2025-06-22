#!/bin/bash

delay=1  # Customize o intervalo entre atualizações
container_name="mosquitto"  # Nome ou ID do contêiner
output_file="mem.dat"

while true; do
    # Extrai CPU e memória usando docker stats (sem TTY)
    docker stats --no-stream --format "{{.CPUPerc}} {{.MemUsage}}" "$container_name" | \
    awk '{gsub(/%/,"",$1); split($2,a,"/"); gsub(/MiB/,"",a[1]); print $1, a[1]}' >> "$output_file"

    gnuplot show_mem.plt
    sleep $delay
done

