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
sudo nano /etc/systemd/system/captchaApi.service
####copy this####
# [Unit]
# Description=captcha API Service
# After=network.target

# [Service]
# User=www-data
# WorkingDirectory=/var/www/scripts
# ExecStart=/usr/bin/python3 /var/www/scripts/captchaApi.py
# Restart=always

# [Install]
# WantedBy=multi-user.target

####################
sudo systemctl daemon-reload
sudo systemctl start captchaApi
sudo systemctl enable captchaApi
sudo systemctl status captchaApi 


