FROM ubuntu:18.04
COPY . ~/projects/anyart_api
WORKDIR ~/projects/anyart_api
EXPOSE 80
RUN "~/projects/anyart_api/deploy.bash"