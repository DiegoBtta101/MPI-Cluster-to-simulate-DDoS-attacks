# 🎯 Diseño e Implementación de un Entorno Distribuido de Simulación y Mitigación de Ataques DDoS mediante Orquestación MPI

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![MPI](https://img.shields.io/badge/Orchestration-MPICH-orange.svg)](https://www.mpich.org/)
[![Ansible](https://img.shields.io/badge/Automation-Ansible-red.svg)](https://www.ansible.com/)
[![Grafana](https://img.shields.io/badge/Monitoring-Grafana-green.svg)](https://grafana.com/)

## 📖 Resumen del Proyecto

Este proyecto documenta la construcción, configuración y operación de un entorno de laboratorio heterogéneo diseñado para simular, monitorizar y mitigar ataques de **Denegación de Servicio Distribuido (DDoS)**. 

El núcleo de la coordinación distribuida utiliza la **Interfaz de Paso de Mensajes (MPI)**, permitiendo la generación de campañas de ataque de alta precisión, volumen y escalabilidad. La observabilidad en tiempo real se garantiza mediante una pila moderna basada en Netdata, Prometheus y Grafana (Dashboard-as-Code).

---

## 🏗️ Arquitectura y Topología de Hardware

La base de este laboratorio de ciberseguridad reside en la heterogeneidad de su hardware, lo que permite observar el comportamiento de los ataques desde la perspectiva de dispositivos con recursos limitados hacia servidores corporativos.

* **Clúster Atacante (Botnet Simulada):** 8 Nodos Raspberry Pi 4 (Orquestados mediante MPICH).
* **Clúster Víctima / Defensivo:** 10 Placas de portátiles bajo Ubuntu Server 22.04 LTS.
* **Red de Computo Dedicada:** `10.4.8.0/24` (Aislamiento de tráfico para evitar cuellos de botella e interferencias externas).

*(Añade aquí fotografías de tu laboratorio si lo deseas)*
---

## 📂 Estructura del Repositorio

La Infraestructura como Código (IaC) y los scripts del proyecto se dividen bajo la siguiente topología de directorios:

```text
├── 00_Diagnostics/       # Scripts y playbooks para pruebas de red y latencia
├── 01_Infrastructure/    # IaC, configuración de nodos y Dashboard-as-Code (JSON)
├── 02_Offensive/         # Scripts de ataque distribuido (HTTP Flood, SYN Flood) vía MPI
├── 03_Defensive/         # Reglas de mitigación, firewalls, y configuraciones Nginx
├── 04_Documentation/     # Memorias técnicas, manuales y bitácoras
├── Plan de Ataque DDoS con MPI.pdf
└── README.md

## ⚙️ Fase 1: Arquitectura de Almacenamiento (NFS)
El clúster ofensivo (Raspberry Pi) utiliza una arquitectura de almacenamiento compartido mediante **NFS (Network File System)**. El directorio `/home` del Nodo Maestro está montado en todos los nodos trabajadores. Esto elimina la necesidad de distribuir manualmente los binarios; cualquier script creado en el maestro está inmediatamente disponible para toda la botnet.

## 🚀 Fase 3: Ejecución de la Simulación Ofensiva
El ataque de demostración principal consiste en un **HTTP Flood (Capa 7)** dirigido al servidor web Nginx de la víctima (`10.4.8.11`). Gracias al NFS, simplemente nos ubicamos en el maestro y disparamos:

```bash
cd ~/mpi_jobs/
/usr/bin/mpiexec.mpich -genv UCX_NET_DEVICES=eth0 -n 32 -f machinefile python3 ddos_orchestrator.py
```