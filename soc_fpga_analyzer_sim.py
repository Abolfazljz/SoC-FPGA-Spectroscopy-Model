import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter, find_peaks

def generate_emulator_pulses(t, fs, rate, mean_amp, sigma_amp, rise_time, fall_time):
    num_points = len(t)
    p_success = rate / fs
    triggers = np.random.binomial(1, p_success, num_points)
    pulse_indices = np.where(triggers == 1)[0]
    
    signal = np.zeros(num_points)
    actual_heights = []
    
    for idx in pulse_indices:
        amp = np.random.normal(mean_amp, sigma_amp)
        if amp < 0: 
            amp = 0
        actual_heights.append(amp)
        
        t_pulse = t[idx:] - t[idx]
        pulse_shape = (np.exp(-t_pulse / fall_time) - np.exp(-t_pulse / rise_time))
        normalization = np.max(pulse_shape)
        if normalization > 0:
            pulse_shape = pulse_shape / normalization
        
        signal[idx:] += amp * pulse_shape
        
    return signal, pulse_indices, actual_heights

def design_triangular_fir(stages):
    half = np.arange(1, stages + 1)
    w = np.concatenate((half, half[-2::-1]))
    return w / np.sum(w)

fs = 125e6
duration = 500e-6
t = np.arange(0, duration, 1/fs)

rate = 40000
mean_amp = 0.7
sigma_amp = 0.12
rise_t = 64e-9
fall_t = 1200e-9

raw_signal, peak_indices, true_amps = generate_emulator_pulses(t, fs, rate, mean_amp, sigma_amp, rise_t, fall_t)
noise = np.random.normal(0, 0.035, len(t))
adc_signal = raw_signal + noise

fir_weights = design_triangular_fir(stages=14)
filtered_signal = lfilter(fir_weights, 1.0, adc_signal)

detected_peaks, props = find_peaks(filtered_signal, height=0.15, distance=int(fs * 150e-9))
detected_heights = filtered_signal[detected_peaks]

fig, axs = plt.subplots(3, 1, figsize=(14, 10))

axs[0].plot(t * 1e6, adc_signal, color='silver', alpha=0.7, label='Raw ADC Signal (Emulator Output)')
axs[0].plot(t * 1e6, filtered_signal, color='crimson', linewidth=1.2, label='Filtered Signal (Triangular FIR)')
axs[0].plot(t[detected_peaks] * 1e6, filtered_signal[detected_peaks], 'x', color='black', markersize=6, markeredgewidth=1.5, label='Captured Heights')
axs[0].set_title('Digital Spectroscopy Channel Simulation', fontsize=12, fontweight='bold')
axs[0].set_xlabel('Time ($\mu$s)')
axs[0].set_ylabel('Amplitude (V)')
axs[0].legend(loc='upper right')
axs[0].grid(True, linestyle=':', alpha=0.6)

zoom_start = int(len(t) * 0.2)
zoom_end = zoom_start + int(fs * 15e-6)
axs[1].plot(t[zoom_start:zoom_end] * 1e6, adc_signal[zoom_start:zoom_end], color='silver', alpha=0.7)
axs[1].plot(t[zoom_start:zoom_end] * 1e6, filtered_signal[zoom_start:zoom_end], color='crimson', linewidth=1.8)
zoom_peaks = detected_peaks[(detected_peaks >= zoom_start) & (detected_peaks < zoom_end)]
axs[1].plot(t[zoom_peaks] * 1e6, filtered_signal[zoom_peaks], 'x', color='black', markersize=9, markeredgewidth=2)
axs[1].set_title('Detailed Waveform Zoom (Pile-up Resolving Performance)', fontsize=11, fontweight='bold')
axs[1].set_xlabel('Time ($\mu$s)')
axs[1].set_ylabel('Amplitude (V)')
axs[1].grid(True, linestyle=':', alpha=0.6)

axs[2].hist(detected_heights, bins=120, range=(0.1, 1.4), color='royalblue', edgecolor='black', alpha=0.75, label='MCA Channels')
axs[2].set_title('Multichannel Analyzer (MCA) Pulse Height Spectrum', fontsize=12, fontweight='bold')
axs[2].set_xlabel('Energy / Digital Peak Value (V)')
axs[2].set_ylabel('Counts')
axs[2].legend(loc='upper right')
axs[2].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()