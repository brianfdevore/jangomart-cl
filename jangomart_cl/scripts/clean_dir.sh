#!/bin/bash
FILE=/var/www/html/index.php
if test -f "$FILE"; then
    rm /var/www/html/index.php
fi