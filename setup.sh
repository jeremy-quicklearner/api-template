#!/bin/bash

# Directory this script is in
ROOTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 -m venv $ROOTDIR
