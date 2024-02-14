#!/bin/bash

sudo chown -R $(whoami) ~/.docker

docker build -t valentin .
docker run -d -p 4000:80 --name valentin valentin


