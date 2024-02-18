#!/bin/bash
echo ------------------------
echo VALENTIN BUILD SETUP
echo ------------------------

cd ./valentin

npm install
npm audit fix --force
npm test -- --watchAll=false

docker-compose up --build

