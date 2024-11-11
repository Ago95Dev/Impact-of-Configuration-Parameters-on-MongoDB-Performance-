# Impact-of-Configuration-Parameters-on-MongoDB-Performance-
Thesis Project on the performance of configuration parameters on MongoDB Performance

## Table of Contents

* [Introduction](#introduction)
* [Requirements](#requirements)
* [Running the Project](#running-the-project)
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
4. The container will run the `main.py` script
5. The `bayes_runtime.py` script will then run, which will perform Bayesian optimization on the generated data, "merged_data.csv" is the dataset.

Note: The `make_df_metrics.py` script is currently not implemented with Docker and will not run correctly in the container. To run this script, you will need to execute it manually outside of the Docker container.

## Known Limitations

* The `make_df_metrics.py` script is not currently compatible with Docker and will not run correctly in the container. This is a known issue and will be addressed in a future update.

I hope this helps! Let me know if you have any questions or need further clarification.