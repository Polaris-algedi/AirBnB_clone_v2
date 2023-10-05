#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# Install Nginx if it not already installed
sudo apt-get update > /dev/null
sudo apt-get -y install nginx > /dev/null

# Create the necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link, deleting old one if it exists
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i "54i \\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default
# IMPORTANT: I In my servers I the one bellow
#sudo sed -i "24i \\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/nginx.conf

# Restart Nginx
sudo service nginx restart
