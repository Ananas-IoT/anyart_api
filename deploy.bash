apt update && apt -y upgrade && apt install -y apache2 lynx python3-pip apache2 libapache2-mod-wsgi-py3 build-essential libssl-dev libffi-dev python3-dev libmysqlclient-dev virtualenv;
sed -i 's/DEBUG = True/DEBUG = False/' /anyart_api/anyart_api/settings.py;
virtualenv -p /usr/bin/python3 /anyart_api/venv;
source /anyart_api/venv/bin/activate;
pip install -r /anyart_api/requirements.txt;
cp /anyart_api/000-default.conf /etc/apache2/sites-available/000-default.conf; 
cp /anyart_api/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf;
python /anyart_api/reload.py;


# mkdir /app;
# cat /etc/apache2/apache2.conf | grep error.log;
# sed -i 's:${APACHE_LOG_DIR}:/app:' /etc/apache2/apache2.conf;
# cat /etc/apache2/apache2.conf | grep error.log;