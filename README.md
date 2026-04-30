# Overview
This project captures suspicious network interactions through a Dionaea honeypot, analyzes them using SLIPS's machine learning-based behavioral detection engine, and forwards structured alerts via Filebeat to Elasticsearch for centralized indexing and Kibana dashboard visualization.

# Architecture
<img width="1169" height="827" alt="architecture" src="https://github.com/user-attachments/assets/1231182d-d058-4034-9d60-16af695223fa" />
This architecture begins when VM1 attempts to send attack traffic to VM4, but the traffic is blocked by the firewall policy on the real server. As a result, the attacker cannot directly access VM4. The suspicious interactions are instead observed through VM2, which acts as the honeypot and analysis node. On VM2, Dionaea captures the attack traffic, SLIPS analyzes the behavior, and Filebeat forwards the generated alert data to VM3. On VM3, Elasticsearch stores and indexes the data, while Kibana visualizes the alerts for centralized monitoring. At the same time, VM4 continues to generate legitimate service logs, which are also sent to VM3 through Filebeat. This design allows the system to separate blocked malicious activity from authorized normal activity within a single SIEM platform.

# Main Components
- Dionaea Honeypot : https://dionaea.readthedocs.io/en/latest/
- Stratosphere Linux IPS (SLIPS): https://stratospherelinuxips.readthedocs.io/
- Filebeat : https://www.elastic.co/docs/reference/beats/filebeat
- Elasticsearch : https://www.elastic.co/docs/reference/elasticsearch
- Kibana : https://www.elastic.co/docs/reference/kibana

# Specification
The proposed system was implemented and tested in a virtualized environment using **Oracle VirtualBox** on the following host machine and virtual machine specifications.

| Component | Specification |
|---|---|
| CPU | AMD Ryzen 7 8845HS w/ Radeon 780M Graphics (16 CPUs), ~3.8 GHz |
| RAM | 16 GB |
| OS | Windows 11 Home Single Language 64-bit |

| VM | Role | CPU | RAM | OS |
|---|---|---:|---:|---|
| VM 2 | Honeypot & Analysis Node | 8 Core | 12 GB | Ubuntu 18.04.6 LTS |
| VM 3 | SIEM Node | 1 Core | 4 GB | Ubuntu 22.04.5 LTS |
| VM 4 | Real Server Node | 1 Core | 2 GB | Ubuntu 22.04.5 LTS |

# Installation
### 1. Update the operating system on each VM
```bash
sudo apt update && sudo apt upgrade -y
```
### 2. Install Docker
Docker is required on VM 2 to run SLIPS & VM 3 to run Elasticsearch and Kibana. Please follow the official Docker installation guide for Ubuntu https://docs.docker.com/engine/install/ubuntu/

### 3. Pull the SLIPS image on VM 2
```bash
docker pull stratosphereips/slips:latest
```

### 3. Pull the ElasticSearch & Kibana image on VM 3
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:9.3.1
docker pull docker.elastic.co/kibana/kibana:9.3.1
```

### 4. Create the SLIPS output directory on VM 2
Create a directory in the home folder to store SLIPS output files:

```bash
mkdir -p ~/slips_out
```

### 5. Customize SLIPS configuration
SLIPS is an open-source tool, so its configuration can be adjusted based on the experimental needs.

In this project, the time window was changed to 5 minutes in order to make detection faster. To modify the time window, open the following configuration file inside the SLIPS environment:
```bash
config/slips.yaml
```

### 6. Install filebeat

```bash
sudo apt install filebeat -y
sudo nano /etc/filebeat/filebeat.yml
```
Edit the filebeat.yml with the file i provided below

# How to Start the System

Before starting the system, make sure all required installation & configurations on **VM 2**, **VM 3**, and **VM 4** have been completed correctly by following the previous step.

### 1. Start all virtual machines
Power on all VMs used in the experiment:
- **VM 1**: Attacker node
- **VM 2**: Honeypot and analysis node
- **VM 3**: SIEM node
- **VM 4**: Real server node

### 2. Start Elasticsearch and Kibana on VM 3
On **VM 3**, start the Elasticsearch and Kibana containers:

```bash
sudo docker start es01 && sudo docker start kib01
```
Wait a few minutes until both services are fully initialized.

### 3. Start Filebeat
Start Filebeat status on VM 2, and VM 4:
```bash
sudo systemctl start filebeat
```

### 4. Verify Elasticsearch service
Still on VM 3, verify that Elasticsearch is running properly:
```bash
curl http://localhost:9200
```
If a JSON response is returned, the service is ready to use.

### 5. Start Dionaea on VM 2
On VM 2, start the Dionaea honeypot service:
```bash
sudo /opt/dionaea/bin/dionaea -l all,-debug -L '*'
```

### 6. Start Dionaea on VM 2
Still on VM 2, run the SLIPS container:
```bash
sudo docker run -d \
  --name slips \
  --net=host \
  -v /home/$USER/slips_out:/StratosphereLinuxIPS/output \
  stratosphereips/slips:latest \
  /StratosphereLinuxIPS/slips.py -i enp0s8
```
You can now perform attack simulations from the attacker machine, such as port scanning, brute-force,dos/ddos, etc

### 7. Monitor alerts
To monitor all the security events and logs forwarded by Filebeat to the SIEM  node, open a web browser on VM 3 and navigate to http://192.168.100.30:5601. This address points to the Kibana web interface hosted on VM 3, which serves  as the centralized dashboard for visualizing all indexed data stored in Elasticsearch.
