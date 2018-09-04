## Makefile for bgpstream docker container

build: Dockerfile
	docker build -t bgp_analysis .

shell: build
	docker run --hostname bgpstream -v $$(pwd)/work:/work -it bgp_analysis:latest /bin/bash

shell2: build
	docker run --hostname opendata -v $$(pwd)/work:/work_ipv6 -it bgp_analysis:latest /bin/bash
