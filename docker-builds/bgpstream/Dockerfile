FROM ubuntu:16.04
# RUN echo 'Acquire::http::Proxy "http://trantor.labs.lacnic.net:9999";' >> /etc/apt/apt.conf.d/00aptproxy
RUN apt-get -y update && apt-get -y install build-essential graphviz zlib1g-dev libbz2-dev libcurl4-openssl-dev python python-pip vim-tiny wget less
# RUN apt-get -y install zlib1g-dev libbz2-dev libcurl4-openssl-dev python python-pip vim-tiny wget less
# RUN apt-get -y install python python-pip vim-tiny wget less
# RUN pip install ipwhois
RUN pip install fire click ipaddr 
RUN pip install consecution
COPY download/* /root/

# Compile dependency WANDIO
WORKDIR /root
RUN tar xzvf wandio-1.0.4.tar.gz
WORKDIR /root/wandio-1.0.4
# WORKDIR /work/src/wandio-1.0.4
RUN ./configure && make && make install && ldconfig


##  Compile bgpstream
WORKDIR /root
RUN tar xzvf bgpstream-1.2.1.tar.gz
WORKDIR /root/bgpstream-1.2.1
RUN ./configure && make && make install && ldconfig
WORKDIR /work
