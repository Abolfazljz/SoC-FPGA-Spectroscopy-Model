# Advanced Digital Spectroscopy Channel Simulation (DSP)

## 📌 Overview
This repository contains a comprehensive Python simulation of a Data Acquisition System for a Digital Spectroscopy Channel, inspired by SoC FPGA architectures. This project was developed as part of the Digital Signal Processing (DSP) course at Science and Research Branch, Islamic Azad University.

The system models both the physical generation of nuclear radiation pulses and the digital signal processing required to analyze them, specifically focusing on resolving pulse pile-up issues using advanced filtering techniques.

## 👨‍💻 Author
**Abolfazl Jafarizadeh**  
*Electrical Engineering (Digital Systems)*

## ⚙️ Project Architecture
The simulation is divided into two primary modules:
1. **Pulse Emulator:** Generates synthetic preamplifier signals. It uses a Binomial distribution to approximate the Poisson nature of radiation events and a Gaussian distribution for pulse amplitudes (energy).
2. **Pulse Analyzer (DSP):** Implements a **Triangular FIR Filter** to process the noisy, overlapping raw signals. This zero-phase distortion filter smooths the rising edges, enabling precise edge detection and accurate pulse height extraction even during severe signal pile-ups.

## 🚀 Features
*   **Statistical Pulse Generation:** Simulates realistic nuclear decay events with background noise.
*   **Pile-up Resolution:** Successfully detects and separates overlapping pulses that occur within nanoseconds of each other.
*   **Multichannel Analyzer (MCA):** Generates a Gaussian energy spectrum histogram from the extracted pulse heights, mimicking real-world laboratory equipment.

## 💻 How to Run

1. Clone this repository or download the `digital_spectroscopy_dsp.py` file.
2. Install the required computational dependencies:
   ```bash
   pip install numpy scipy matplotlib
Execute the simulation script:

   ```Bash
   python digital_spectroscopy_dsp.py
   ```
The script will generate a high-resolution, three-panel plot showcasing the raw signal, the zoomed-in pile-up resolution, and the final MCA energy spectrum.

## 📄 Documentation
The repository also includes translated documentation and a comprehensive lab report analyzing the FIR filter's performance and the statistical models used in the simulation.
