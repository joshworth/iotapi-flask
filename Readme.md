Alembic Migrations -Initial
alembic revision --autogenerate -m "First commit"


Setup
==========================

# 1. update your local packages
    $ sudo apt-get update

# 2. install dependencies
    $ sudo apt-get install python3-pip python3-dev nginx

# 2.1 Setup and  Configure app
    -Create app directory iotapi wih dev contents
    - setup db conection in iotapi conf/app.yaml    

# 3. Create venv
    $ cd iotapi
    $ python3 -m venv venv

# 4. install requirements
    $ source venv/bin/activate
    $ pip3 install -r requirements

# 5. Create file wsgi.py
    test,
    $ gunicorn --bind 0.0.0.0:5000 wsgi:iotapp

# 6. create unit file for  service
    $ sudo nano /etc/systemd/system/iotapi.service
    test, 
    $ lynx http://0.0.0.0:5000

# 7. launch service
    $ sudo systemctl start iotapi
    $ sudo systemctl enable iotapi
    confirm that there is a unix socket , iotapi.sock ,  created in app directory
    
    $ sudo systemctl stop iotapi
    $ sudo systemctl status iotapi

# 8. Configure nginx, create site conf file
    $ sudo nano /etc/nginx/sites-available/iotapi.conf
    $ sudo ln -s /etc/nginx/sites-available/iotapi.conf /etc/nginx/sites-enabled

# 9. Bounce nginx
    $ sudo systemctl restart nginx
    $ sudo systemctl status nginx
    $ sudo systemctl start nginx
    $ sudo systemctl stop nginx

# 10. Allow nginx and port in firewall
    $ sudo ufw status verbose
    $ sudo ufw allow 'Nginx Full'
    $ sudo ufw allow 8088/tcp


    


    





permissions
============
sudo chown -R ubuntu:www-data iotapi/


tools:
=========
- lynx for terminal browsing


issues:
==============
ImportError: cannot import name 'jwt_refresh_token_required'

encoding stuff in login gives error on linux
    'accessToken': token.decode('UTF-8') causes issues, change to 'accessToken': token,


gunicorn --bind 0.0.0.0:5000 wsgi:iotapi

cors issues:
===============
- enable cors on flask and not nginx to avoid double header errors
- if you enable cors on nginx, do not enable on flask, this will create double header that will be rejected by browser


support
sudo less /var/log/nginx/error.log: checks the Nginx error logs.
sudo less /var/log/nginx/access.log: checks the Nginx access logs.
sudo journalctl -u nginx: checks the Nginx process logs.
sudo journalctl -u iotapi: checks your Flask app’s uWSGI logs. pipe to file



psql:
1. Connect $ psql -d postgres -U postgres
2. List db and conncect
    # \l 
    # \c iot_db
3. List tables
    # \dt
4. List roles, users
    # \dg
    
--- users
CREATE DATABASE iot_db;
CREATE USER iotapiman WITH PASSWORD 'man@10tapi';
GRANT ALL PRIVILEGES ON DATABASE iot_db TO iotapiman;



--migrate data from lite to psql
dump from lite to csv, then import from psql, maintain the column count in the csv as in the query

$sqlite3 iot.db
    # .headers on
    # .output 
    # select device_name,device_type,barcode,created_on from device;

$psql
    # \COPY dtube(device_name,device_type,barcode,created_on) from '/home/ubuntu/ngroot/iotapi/qqq1.txt' delimiter '|' csv header;

