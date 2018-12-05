## Makefile for bgpstream docker container

help: 
	echo "build: build docker images"
	echo "ipv6pfxvis: IPv6 prefix visibility over time"

build: ./docker-builds/bgpstream/Dockerfile 
	docker build -t bgp_stream ./docker-builds/bgpstream

ipv6pfxvis: build
	docker run --hostname ipv6visibility  \
			-v $$(pwd)/ipv6-pfx-visibility/work:/work \
			-v $$(pwd)/ipv6-pfx-visibility/scripts:/scripts:ro \
			-v $$(pwd)/data:/data:ro  -it bgp_stream:latest /bin/bash || /bin/true

ipv6rttoday: build
	date +"%Y%m%d" > $$(pwd)/ipv6-pfx-visibility/work/target_today.txt	
	docker run --hostname ipv6visibility  \
			-v $$(pwd)/ipv6-pfx-visibility/work:/work \
			-v $$(pwd)/ipv6-pfx-visibility/scripts:/scripts:ro \
			-v $$(pwd)/data:/data:ro bgp_stream:latest /scripts/process_ipv6_routing_data.py /work/target_today.txt  || /bin/true

