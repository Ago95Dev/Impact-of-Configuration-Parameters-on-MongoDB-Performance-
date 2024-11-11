# Impact-of-Configuration-Parameters-on-MongoDB-Performance-
Thesis Project on the performance of configuration parameters on MongoDB Performance

## Table of Contents

* [Introduction](#introduction)
* [Requirements](#requirements)
* [Running the Project](#running-the-project)
* [Script Description](#script-description)
* [Known Limitations](#known-limitations)

## Introduction

This project investigates the impact of configuration parameters on MongoDB performance. It uses a combination of benchmarking tools and Algorithm optimization to identify the optimal configuration for a given workload.

## Requirements

* Python 3.10
* Docker
* MongoDB
* YCSB (Yahoo! Cloud Serving Benchmark)

## Running the Project

1. Clone the repository and navigate to the project directory.
2. Build the Docker image by running `docker-compose build`.
3. Start the Docker container by running `docker-compose up`.
4. The container will run the `main.py` script, printing "Docker setup is working!". (debug code)
5. The `bayes_runtime.py` script will then run, which will perform Bayesian optimization on the generated data, "merged_data.csv" is the dataset.

Note: The `make_df_metrics.py` script is currently not implemented with Docker and will not run correctly in the container. To run this script, you will need to execute it manually outside of the Docker container.

## Script Description

make_df_metrics.py
Il file make_df_metrics.py è responsabile della creazione di un DataFrame contenente le metriche di prestazioni del database. Questo script legge i dati generati dal benchmark e li elabora per creare un DataFrame che può essere utilizzato per l'ottimizzazione bayesiana. Nota: Questo script non è attualmente compatibile con Docker e deve essere eseguito manualmente al di fuori del container.

bayes_runtime.py
Il file bayes_runtime.py esegue l'ottimizzazione bayesiana sui dati generati dal benchmark. Questo script utilizza la libreria skopt per eseguire l'ottimizzazione e identificare la configurazione ottimale per il database

## Known Limitations

* The `make_df_metrics.py` script is not currently compatible with Docker and will not run correctly in the container. This is a known issue and will be addressed in a future update.

I hope this helps! Let me know if you have any questions or need further clarification.