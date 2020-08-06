#!/bin/bash
yum update -y
yum install -y httpd
yum install -y php
yum install -y wget 

cd /var/www/html
wget https://raw.githubusercontent.com/brianfdevore/jangomart-cl/master/website/index.php
wget https://raw.githubusercontent.com/brianfdevore/jangomart-cl/master/website/htaccess
mv /var/www/html/htaccess /var/www/html/.htaccess

checkconfig httpd on
sudo systemctl start httpd
sudo systemctl enable httpd
sudo usermod -a -G apache ec2-user
sudo chown -R ec2-user:apache /var/www
sudo chmod 2775 /var/www && find /var/www -type d -exec sudo chmod 2775 {} \;
find /var/www -type f -exec sudo chmod 0664 {} \;