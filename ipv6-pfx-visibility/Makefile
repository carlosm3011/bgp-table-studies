## Makefile for bgpstream docker container

build: Dockerfile
	docker build -t bgp_analysis .

shell: build
	docker run --hostname ipv6visibility  -v $$(pwd)/work:/work -v $$(pwd)/../data:/data  -it bgp_analysis:latest /bin/bash

