#!/usr/bin/env bash

ffprobe -v quiet -print_format json -show_format -show_streams "$1"