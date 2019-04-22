FROM ubuntu:18.04
COPY . /anyart_api
EXPOSE 80
RUN /bin/bash -c "/anyart_api/deploy.bash"
CMD ["apache2ctl", "-D", "FOREGROUND"]