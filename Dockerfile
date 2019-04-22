FROM ubuntu:18.04
COPY . /anyart_api
# WORKDIR ~/projects/anyart_api
EXPOSE 80
RUN "/anyart_api/deploy.bash"