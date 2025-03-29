# Out of Order and Causally Correct: Ready-Event Discovery through Data-Dependence Analysis

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## ACM SIGSIM-PADS 25 (2025)

This repository contains the artifacts for our paper "Out of Order and Causally Correct: Ready-Event Discovery through Data-Dependence Analysis" presented at ACM SIGSIM-PADS 25.

## Setup with Docker

### Prerequisites
- Docker
- Docker Compose (optional, for easier management)

### Building and Running with Docker

1. **Build the Docker image and start the container**:
   ```bash
   docker build -t pads-artifact .
   docker-compose up -d
   ```

2. **Enter the container and run the scripts**:
   ```bash
   # Enter the container
   sudo docker-compose exec pads-artifact bash
   
   # Inside the container, make the script executable and run it
   chmod +x run.sh
   ./run.sh
   ```

   This will:
   - Compile the code
   - Run the simulation experiments
   - Generate plots based on the results

## Artifact Structure

- `OoO_Sim`: Main simulation binary (compiled from C++ sources)
- `PADS_resilient_auto_testing.py`: Script to run simulations with various parameters
- `PADS_plot_REs_64.py`, `PADS_plot_REs_729.py`, `PADS_plot_order_diffs_64.py`: Scripts to generate figures
- Supporting directories:
  - `exec_orders/`: Execution order data
  - `input_files/`: Simulation input configurations
  - `output_files/`: Simulation outputs
  - `params_files/`: Parameter files for simulations
  - `traces/`: Trace files from simulation runs
  - `ITL_tables/`: Tables for analysis

## Running Experiments

1. **Compile the code** (already done in the Docker build):
   ```bash
   make
   ```

2. **Run the automatic testing script**:
   ```bash
   python3 PADS_resilient_auto_testing.py
   ```
   
   > **Note:** In `PADS_resilient_auto_testing.py`, the `max_workers` parameter controls how many simulation runs are executed in parallel. Adjust this value based on your system's CPU and memory constraints.

3. **Generate plots** after simulations complete:
   ```bash
   python3 PADS_plot_REs_64.py
   python3 PADS_plot_REs_729.py
   python3 PADS_plot_order_diffs_64.py
   ```

4. **Run the simple DIR simulation**:
   ```bash
   python3 PADS25_python_sim_nQ_DIR.py
   ```

## Artifact Description

This artifact contains the code used to run the simulations described in the paper. The main components are:

1. **OoO_Sim**: A C++ implementation of the simulation engine that supports both in-order and out-of-order execution.

2. **Network Models**:
   - 1D Ring Network (`Ring_1D/`)
   - 2D Grid Network with Von Neumann neighborhood (`Grid_VN2D/`)
   - 3D Grid Network with Von Neumann neighborhood (`Grid_VN3D/`)
   - 3D Torus Network (`Torus_3D/`)

3. **Analysis Scripts**:
   - `PADS_resilient_auto_testing.py`: Runs simulations with different network configurations and parameters
   - `PADS_plot_REs_64.py`: Generates plots for 64-node networks
   - `PADS_plot_REs_729.py`: Generates plots for 729-node networks
   - `PADS_plot_order_diffs_64.py`: Analyzes execution order differences
   - `PADS25_python_sim_nQ_DIR.py`: Simple Python simulation for the DIR algorithm

## Figure and Table Reproduction

The artifact reproduces the following figures and tables from the paper:

### Figure 6
Generated by `PADS_plot_REs_64.py` and `PADS_plot_REs_729.py`

### Figure 7
Generated by `PADS_plot_order_diffs_64.py`

> **Note:** The C++ simulator code that generates the data required for Figure 7 has been commented out (as it's very slow to run). To enable this functionality:
> 
> 1. In `OoO_EventSet.cpp`, uncomment the block-commented code in:
>    - `void OoO_EventSet::ExecuteSerial()` - Look for "// Serial IO execution order"
>    - `void OoO_EventSet::ExecuteSerial_OoO()` - Look for "// Serial OoO execution order"
> 
> 2. Output from running with this code uncommented is already provided in the `exec_orders/` directory.

### Table 2
Generated by running `PADS25_python_sim_nQ_DIR.py`

### Table 5
Generated by `PADS_plot_REs_64.py` and `PADS_plot_REs_729.py` (also generate CSV files)

### Table 6
Generated by `PADS_plot_order_diffs_64.py` (also generates CSV file)

## Extending the Artifact

To run with different parameters, modify the `NETWORK_CONFIGS`, `HOP_RADIUS_VALUES`, or other parameters in `PADS_resilient_auto_testing.py`.


## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

This license requires that modifications to this code must be made available under the same license, even when the code is only used to provide a service over a network without distributing the actual code.
