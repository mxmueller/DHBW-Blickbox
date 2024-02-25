#!/bin/bash
echo ------------------------
echo VALENTIN BUILD SETUP
echo ------------------------

cd ./valentin
npm install 

echo ------------------------
echo TESTING VALENTIN BEFORE DEPLYOMENT
echo ------------------------

npm test -- --watchAll=false

echo ------------------------
echo DEPLOYING DOCKER
echo ------------------------

docker-compose up --build

