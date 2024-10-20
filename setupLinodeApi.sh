sudo apt update
sudo apt upgrade
apt install python3
apt install python3-pip
pip install flask
cd /var/www/scripts
sudo nano linodeApi.py #copy the file
sudo chown -R www-data:www-data /var/www/scripts
sudo chmod +x /var/www/scripts/linodeApi.py
sudo chmod -R 755 /var/www/scripts
python3 linodeApi.py
#test if works
sudo nano /etc/systemd/system/linodeApi.service
####copy this####
# [Unit]
# Description=lindode API Service
# After=network.target

# [Service]
# User=www-data
# WorkingDirectory=/var/www/scripts
# ExecStart=/usr/bin/python3 /var/www/scripts/linodeApi.py
# Restart=always

# [Install]
# WantedBy=multi-user.target

####################
sudo systemctl daemon-reload
sudo systemctl start linodeApi
sudo systemctl enable linodeApi
sudo systemctl status linodeApi 
#####################
#now php:
sudo apt install apache2
sudo apt install php php-cli php-common
sudo systemctl start apache2
sudo systemctl enable apache2
sudo systemctl status apache2
sudo ufw allow http
sudo ufw allow https
sudo ufw reload
sudo systemctl restart apache2
sudo chown www-data:www-data /var/www/html/
sudo chmod 755 /var/www/html/


