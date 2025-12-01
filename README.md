# Cloud-Based Distributed Honeynet & Behavioral Analysis

## Project Overview
This research project deploys a distributed honeynet on AWS EC2 to analyze the behavioral differences between automated botnets and human attackers.

## Architecture
* **Node A (Gateway):** AWS EC2 (Ubuntu). Port 22 (Honeypot) / Port 22222 (Admin).
* **Node B (Target):** Hidden Database Node.

## Features
* **Deception:** Custom AI-generated lures (Salary/Inventory data) injected via Volume Mounts.
* **Forensics:** Persistent JSON logging and HASSH fingerprinting.

## Usage
1. Run 'analysis_tool.py' to parse logs.
2. Run 'ml_model.py' to train the classifier.