# Microfluidic Fully Programmable Valve Array (FPVA) Biochip Sample Preparation Readme

This repository contains code and information related to the implementation of a sample preparation method using Microfluidic Fully Programmable Valve Array (FPVA) biochips. The proposed method aims to optimize the fluid loading process for mixing reagents in a desired ratio through a sequence of mixing steps. The key contributions of this work include the **genMix algorithm** for generating mixing trees, a permutation strategy to simplify fluid loading paths, and the utilization of **LAFCA+DFL** for efficient parallel loading of reagents.

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Code Overview](#code-overview)
- [Usage](#usage)
- [Results](#results)
- [Contributors](#contributors)
- [License](#license)

## Introduction

Microfluidic Fully Programmable Valve Array (FPVA) biochips have gained attention for their potential to perform complex biochemical reactions in a miniaturized format. This repository presents a novel approach to optimize the sample preparation process on FPVA biochips. The key steps include generating mixing trees using the **genMix algorithm**, permuting the tree to minimize reagent usage, and employing **LAFCA+DFL** for efficient reagent loading.

## Requirements

To run the code in this repository, you need the following:

- Python (>= 3.6)
- Libraries: `numpy`, `networkx`, `matplotlib` (for visualization)
- Simulation environment for microfluidic chip behavior (not provided in this repository)

## Code Overview

1. **genMix Algorithm**: The `genMix` algorithm is responsible for generating mixing trees that represent the sequence of mixing steps required to achieve the desired reagent ratios. The algorithm's logic is implemented in the `genMix.py` script.

2. **Permutation Strategy**: The generated mixing tree is then permuted to minimize the number of different reagents under any internal node. This permutation aims to simplify fluid loading paths and reduce sample preparation time. The permutation logic is implemented in the `permuteTree.py` script.

3. **LAFCA+DFL**: The **LAFCA+DFL** algorithm is employed for the parallel loading of reagents at any given time. This ensures efficient fluid loading, reducing the time and cost of sample preparation. The implementation of this algorithm is found in the `LAFCA_DFL.py` script.

## Usage

1. Clone this repository to your local machine.
   
2. Navigate to the repository directory and ensure you have the required libraries installed:

   ```bash
   pip install numpy networkx matplotlib
   ```

3. Use the provided scripts to generate mixing trees, permute the trees, and simulate the LAFCA+DFL process on a microfluidic chip (simulation environment not provided in this repository).

4. Modify the scripts as needed to match your specific microfluidic chip's characteristics and simulation environment.

## Results

The simulation results obtained by applying the proposed algorithm to the mixing tree are detailed in the paper associated with this repository. The results showcase a significant speedup in fluid loading time and savings in reagent usage.

## Contributors

This work was developed by [Author Name(s)] in collaboration with [Institution/Team Name]. If you have any questions, feel free to contact [Author Name(s)] at [contact@email.com].

## License

This project is licensed under the [License Name]. See the [`LICENSE`](LICENSE) file for more details.
