FROM ubuntu:18.04
COPY . /anyart_api
EXPOSE 80
RUN apt update && apt -y upgrade && apt install -y apache2 lynx python3-pip apache2 libapache2-mod-wsgi-py3 build-essential libssl-dev libffi-dev python3-dev virtualenv
RUN sed -i 's/DEBUG = True/DEBUG = False/' ~/projects/anyart_api/anyart_api/settings.py
RUN virtualenv -p /usr/bin/python3 ~/projects/anyart_api/venv
RUN source ~/projects/anyart_api/venv/bin/activate
RUN pip install -r requirements.txt
RUN python reload.py
# RUN CMD ["apache2ctl", "-D", "FOREGROUND"]
RUN cp /home/gursky_michael1999/projects/anyart_api/000-default.conf /etc/apache2/sites-available/000-default.conf 
RUN cp /home/gursky_michael1999/projects/anyart_api/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
RUN mkdir /app;
RUN cat /etc/apache2/apache2.conf | grep error.log
RUN sed -i 's:${APACHE_LOG_DIR}:/app:' /etc/apache2/apache2.conf
RUN cat /etc/apache2/apache2.conf | grep error.log

CMD /bin/bash
