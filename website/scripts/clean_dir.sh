#!/bin/bash

isExistFile = 'find /var/www/html/index.php'

if [[ -n $isExistFile ]]; then
    rm /var/www/html/index.php
fi
