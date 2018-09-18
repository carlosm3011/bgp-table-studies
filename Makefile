## Makefile for bgpstream docker container

build: ./docker-builds/bgpstream/Dockerfile 
	docker build -t bgp_stream ./docker-builds/bgpstream

shell: build
	docker run --hostname ipv6visibility  \
			-v $$(pwd)/ipv6-pfx-visibility/work:/work \
			-v $$(pwd)/ipv6-pfx-visibility/scripts:/scripts:ro \
			-v $$(pwd)/data:/data:ro  -it bgp_stream:latest /bin/bash || /bin/true

