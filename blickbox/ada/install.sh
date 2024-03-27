#!/bin/bash

echo "Compiling ada executeble"
cargo build --release

echo "Creating directory in /usr/local/ada"
sudo mkdir /usr/local/ada
sudo chown blickbox:blickbox /usr/local/ada
sudo chmod 755 /usr/local/ada

echo "copying compiled ada executeable"
cp ./target/release/ada /usr/local/ada

echo "Adding ada executeble to systemd"
sudo cp ./ada.service /etc/systemd/system/ada.service
sudo systemctl enable ada.service
sudo systemctl start ada.service
