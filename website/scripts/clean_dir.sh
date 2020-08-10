#!/bin/bash

isExistFile = "/var/www/html/index.php"

if [[ -e "$isExistFile" ]]
then
    rm /var/www/html/index.php
fi