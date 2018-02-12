# GullinBackend
Gullin Django Based Backend

```
Development

sudo amazon-linux-extras enable python3
sudo amazon-linux-extras enable nginx1.12

cd ~
git clone git@github.com:GullinPlatform/GullinBackend.git

mkdir ~/GullinBackend/Gullin/settings/securities
cd ~/GullinBackend/Gullin/settings/securities

touch aws_secret_key
# add aws key
touch django_secret_key
# add django key

ssh-keygen -t rsa -b 4096 -f jwt_secret.key
openssl rsa -in jwt_secret.key -pubout -outform PEM -out jwt_secret.key.pub

vi ~/GullinBackend/Gullin/settings/prod.py
# Add DB Info

pip install -r requirements.txt

sudo wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
sudo yum localinstall mysql57-community-release-el7-11.noarch.rpm 
sudo yum install mysql-community-server
sudo yum install mysql-devel
sudo yum install python3-devel
sudo pip3 install mysqlclient

python3 manage_prod.py makemigrations
python3 manage_prod.py migrate

sudo yum install nginx
sudo pip3 install uwsgi

cd ~Gullin/
touch nginx_gullin.conf
# change nginx_gullin.conf
touch uwsgi_gullin.ini
# change uwsgi_gullin.ini
touch uwsgi_params
# change uwsgi_params

sudo mkdir /etc/nginx/sites-enabled/
sudo ln -s /home/ec2-user/GullinBackend/nginx_gullin.conf /etc/nginx/sites-enabled/

sudo vi /etc/nginx/nginx.conf
# change user to ec2-user
# add include /etc/nginx/sites-enabled/*;

sudo service nginx start

uwsgi --ini uwsgi_gullin.ini --logto /tmp/gullin.log
```
