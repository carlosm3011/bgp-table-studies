FROM ubuntu:16.04
RUN echo 'Acquire::http::Proxy "http://trantor.labs.lacnic.net:9999";' >> /etc/apt/apt.conf.d/00aptproxy
RUN apt-get -y update && apt-get -y install build-essential graphviz
RUN apt-get -y install zlib1g-dev libbz2-dev libcurl4-openssl-dev
RUN apt-get -y install python python-pip vim-tiny wget less
# RUN pip install ipwhois
RUN pip install fire click ipaddr 
RUN pip install consecution
# RUN pip install apache-airflow cryptography fernet
# RUN pip install snakemake snaketools 
# RUN pip install click
# RUN pip install ipaddr
COPY download/* /root/
WORKDIR /root
RUN tar xzvf wandio-1.0.4.tar.gz
WORKDIR /root/wandio-1.0.4
# WORKDIR /work/src/wandio-1.0.4
RUN ./configure && make && make install && ldconfig
WORKDIR /root
RUN tar xzvf bgpstream-1.1.0.tar.gz
WORKDIR /root/bgpstream-1.1.0
RUN ./configure && make && make install && ldconfig
WORKDIR /work
ENV AIRFLOW_HOME=/work/airflow
# RUN airflow initdb