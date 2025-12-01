#!/bin/bash
# Deployment Script
# 1. Setup Dirs
mkdir -p ~/live_honeyfs/etc
mkdir -p ~/cowrie_logs
touch ~/live_honeyfs/etc/motd

# 2. Launch Container
sudo docker run -d --restart always -p 22:2222 -v /home/ubuntu/live_honeyfs:/cowrie/cowrie-git/honeyfs/root -v /home/ubuntu/cowrie_logs:/cowrie/cowrie-git/var/log/cowrie --name public_honeypot cowrie/cowrie

# 3. Inject Lure
cat ~/live_honeyfs/salary_2025.csv | sudo docker exec -i public_honeypot sh -c 'cat > /cowrie/cowrie-git/honeyfs/etc/motd'