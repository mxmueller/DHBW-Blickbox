#!/bin/bash
echo ------------------------
echo VALENTIN LOCAL DEV SETUP
echo ------------------------

npm test -- --watchAll=false

echo ------------------------
echo VALENTIN JEST TESTS
echo ------------------------

echo "Press Enter to continue..."
read
echo "Continuing..."

npm start
