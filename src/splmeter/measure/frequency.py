from numpy import array as ndarray
from scipy.fft import fft, fftfreq
from scipy.stats import binned_statistic
import numpy as np

from typing import Any

def tofrequencydomain(signal,sample_rate,duration,start=0):
        start_sample = start*sample_rate
        spectrum = []
        for i in range(duration):
            a = start_sample + (i*sample_rate)
            b = a + sample_rate
            if b > signal.shape[0]:
                break
            yf = fft(signal[a:b])
            N = sample_rate
            yf = 2.0/N * np.abs(yf[0:N//2])

            spectrum.append(yf)

        
        T = 1/sample_rate
        frequencies = fftfreq(sample_rate, T)[:sample_rate//2]
        return np.array(spectrum),frequencies

def log_rms(data):
    return(np.sqrt(np.sum(np.square(data))))


class OneThirdOctave():

    def __init__(self,processing: list=[]):

        self.processings = processing
        self.bins = [
                    14.1,
                    17.8,
                    22.4,
                    28.2,
                    35.5,
                    44.7,
                    56.2,
                    70.8,
                    89.1,
                    112,
                    141,
                    178,
                    224,
                    282,
                    355,
                    447,
                    562,
                    708,
                    891,
                    1122,
                    1413,
                    1778,
                    2239,
                    2818,
                    3548,
                    4467,
                    5623,
                    7079,
                    8913,
                    11220,
                    14130,
                    17780,
                    22390
                    ]

    def __call__(self, signal: ndarray, sample_rate: int, duration: int, start: int=0,reference_pressure = 2.0e-5) -> Any:
    
        for processing in self.processings:
            signal = processing(signal)

        spectrum, frequencies = tofrequencydomain(signal,sample_rate,duration,start=start)
        bin_stats, bin_edges, binnumber = binned_statistic(frequencies,spectrum,statistic=log_rms,bins=self.bins)
        freq_data = (20*np.log10(bin_stats/reference_pressure)).T
        return freq_data
    
