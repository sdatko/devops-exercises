#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

#
# Variables
#
APP_PORT=5000
SERVER_LOG=".${0}.log"
SERVER_PID=-1


#
# Cleanup function for the script, trap ensures to execute it
#
function cleanup() {
    if [ "${SERVER_PID}" -gt 0 ]; then
        kill "${SERVER_PID}"
    fi
}
trap cleanup EXIT


#
# Find random ununsed port
#
limit=20
for trial in $(seq 1 "${limit}"); do
    APP_PORT=$(( ( ${RANDOM} + 8000 ) % 65535 ))
    if ! ( echo '' > "/dev/tcp/127.0.0.1/${APP_PORT}" >/dev/null 2>&1 ); then
        break
    fi
    if [ "${trial}" -ge "${limit}" ]; then
        exit 1
    fi
done
export APP_PORT


#
# Run server in a subprocess
#
flask run --port "${APP_PORT}" >"${SERVER_LOG}" 2>&1 &
SERVER_PID=$!


#
# Launch the tests
#
python3 -m pytest --verbose --capture=no tests-functional.py
