# Overview
This project captures suspicious network interactions through a Dionaea honeypot, analyzes them using SLIPS's machine learning-based behavioral detection engine, and forwards structured alerts via Filebeat to Elasticsearch for centralized indexing and Kibana dashboard visualization.

## Architecture
<img width="1169" height="827" alt="architecture" src="https://github.com/user-attachments/assets/1231182d-d058-4034-9d60-16af695223fa" />

## Main Components
- Dionaea Honeypot : https://dionaea.readthedocs.io/en/latest/
- Stratosphere Linux IPS (SLIPS): https://stratospherelinuxips.readthedocs.io/
- Filebeat : https://www.elastic.co/docs/reference/beats/filebeat
- Elasticsearch : https://www.elastic.co/docs/reference/elasticsearch
- Kibana : https://www.elastic.co/docs/reference/kibana
