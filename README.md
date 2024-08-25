# Optical-Network-Simulation
Routing and Spectrum Assignment in Optical Network

# Optical Network Simulation

This project implements a comprehensive optical network simulation framework with various resource allocation algorithms, including Reinforcement Learning (RL), Deep Reinforcement Learning (DRL), Multi-Agent Reinforcement Learning (MARL), and traditional heuristics. The simulation also includes Quantum Key Distribution (QKD) integration and telemetry collection capabilities.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Algorithms](#algorithms)
8. [QKD Integration](#qkd-integration)
9. [Telemetry and Telegraf Integration](#telemetry-and-telegraf-integration)
10. [Results Analysis](#results-analysis)
11. [Contributing](#contributing)
12. [License](#license)

## Overview

This simulation framework models an optical network and explores various resource allocation strategies for efficient spectrum usage, path selection, and modulation format assignment. It incorporates advanced techniques such as Reinforcement Learning and Quantum Key Distribution to optimize network performance and security.

## Features

- Multiple resource allocation algorithms: RL, DRL, MARL, k-Shortest Path, Load Balancing
- Spectrum assignment strategies: First Fit, Random Fit
- Quantum Key Distribution (QKD) integration
- Telemetry collection and Telegraf integration
- Customizable network topology (default: German Backbone Network)
- Flexible traffic generation
- Comprehensive result analysis and visualization

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/optical-network-simulation.git
   cd optical-network-simulation
   ```

2. Install required dependencies:
   ```
   pip install numpy pandas matplotlib networkx scipy tensorflow tqdm
   ```

## Project Structure

The main components of the simulation are:

- `OpticalNetworkSimulator`: The core simulation class
- `PathComputation`: Handles path computation and related operations
- `SpectrumManagement`: Manages spectrum allocation and related functions
- `QKDManagement`: Handles Quantum Key Distribution operations
- `RLManagement`: Implements RL, DRL, and MARL algorithms
- `TelemetryManagement`: Manages telemetry collection and processing

## Configuration

The simulation can be configured using various parameters:

- Network parameters (e.g., topology, fiber properties)
- Traffic parameters (e.g., load, request distribution)
- Algorithm-specific parameters (e.g., RL hyperparameters)
- QKD parameters
- Simulation settings (e.g., duration, real-time mode)


## Usage

To run a simulation:

1. Set up the configuration parameters.
2. Initialize the `OpticalNetworkSimulator` with desired settings.
3. Call the `simulate()` method.
4. Analyze the results.

Example:

```python
simulator = OpticalNetworkSimulator(
    topology=create_german_backbone_topology(),
    traffic_load=500,
    simulation_time=1,
    constants=constants,
    mu_rate=mu_rate,
    org_qkd_keys_dict=org_qkd_keys_dict,
    qkd_keys_dict=qkd_keys_dict,
    qkd_params=qkd_params,
    drl_params=drl_params,
    marl_params=marl_params,
    modulation_bits_per_symbol=modulation_bits_per_symbol,
    modulations_gsnr_thresholds=modulations_gsnr_thresholds,
    request_bit_rates=request_bit_rates,
    fiber_params=fiber_params,
    edfa_params=edfa_params,
    roadm_params=roadm_params,
    transceiver_params=transceiver_params,
    channel_params=channel_params,
    wavelength_continuity=True,
    path_selection='LB',
    spectrum_assignment='FF',
    seed=2024,
    real_time_simulation=False,
    telemetry_collection=True
)

simulator.simulate()
results = simulator.get_results()
```

## Algorithms

### Reinforcement Learning (RL)

Uses Q-learning to make decisions about path selection, modulation format, and spectrum allocation.

### Deep Reinforcement Learning (DRL)

Employs a neural network to approximate the Q-function for improved learning in high-dimensional state spaces.

### Multi-Agent Reinforcement Learning (MARL)

Utilizes multiple RL agents, each associated with a network node, to make collaborative decisions.

### k-Shortest Path (kSP)

Computes the k shortest paths between source and destination nodes, considering physical distance and network constraints.

### Load Balancing (LB)

Aims to distribute network traffic evenly across available resources to prevent congestion.

### First Fit (FF) and Random Fit (RF)

Spectrum assignment algorithms for allocating frequency slots to connection requests.

## QKD Integration

The simulation integrates Quantum Key Distribution (QKD) to enhance network security. QKD-related operations are handled by the `QKDManagement` class, which simulates key generation, distribution, and consumption.

## Telemetry and Telegraf Integration

The simulation includes telemetry collection capabilities that can be integrated with Telegraf for real-time monitoring and analysis. To enable telemetry collection, set `telemetry_collection=True` when initializing the simulator.

For Telegraf integration, configure the Telegraf input plugin to read the generated metrics file:

```toml
[[inputs.file]]
  files = ["path/to/your/<algorithm>_<load>_network_metrics.txt"]
  data_format = "influx"
```

## Results Analysis

The simulation provides comprehensive results, including:

- Blocking probability
- Spectrum usage
- Power consumption
- Path usage statistics
- QKD key consumption
- Detailed connection information

Use the provided plotting functions or custom scripts to visualize and analyze the results.
