#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

readonly TARGET_HOST=blickbox@blickbox.local
readonly TARGET_PATH=/home/pi/hello-world
readonly SOURCE_PATH=./target/release/hello-world

cargo build --release
rsync ${SOURCE_PATH} ${TARGET_HOST}:${TARGET_PATH}
ssh -t ${TARGET_HOST} ${TARGET_PATH}