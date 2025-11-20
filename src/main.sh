#!/bin/bash
./bootup_logo.sh

python -c "from bootloader_package.bootloader import Boot
Boot()"
