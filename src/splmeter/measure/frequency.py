from numpy import array as ndarray
from scipy.fft import fft, fftfreq
from scipy.stats import binned_statistic
import numpy as np

from typing import Any

def tofrequencydomain(signal,sample_rate):
        # start_sample = start*sample_rate
        spectrum = []

        for a in range(sample_rate,signal.shape[0]+1,sample_rate):
             
            b = a - sample_rate
            yf = fft(signal[b:a])
            N = sample_rate
            yf = 2.0/N * np.abs(yf[0:N//2])

            spectrum.append(yf)




        # for i in range(duration):
        #     a = start_sample + (i*sample_rate)
        #     b = a + sample_rate
        #     if b > signal.shape[0]:
        #         break
        #     yf = fft(signal[a:b])
        #     N = sample_rate
        #     yf = 2.0/N * np.abs(yf[0:N//2])

        #     spectrum.append(yf)

        
        T = 1/sample_rate
        frequencies = fftfreq(sample_rate, T)[:sample_rate//2]
        return np.array(spectrum),frequencies

def log_rms(data):
    return(np.sqrt(np.sum(np.square(data))))


class OneThirdOctave():

    def __init__(self,reference_pressure = 2.0e-5):
        self.reference_pressure = reference_pressure
        # self.processings = processing
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
        
        self.bin_names = [
                            16,
                            20,
                            25,
                            31.5,
                            40,
                            50,
                            63,
                            80,
                            100,
                            125,
                            160,
                            200,
                            250,
                            315,
                            400,
                            500,
                            630,
                            800,
                            1000,
                            1250,
                            1600,
                            2000,
                            2500,
                            3150,
                            4000,
                            5000,
                            6300,
                            8000,
                            10000,
                            12500,
                            16000,
                            20000,
                            ]

    def __call__(self, signal: ndarray, sample_rate: int) -> Any:
    
        # for processing in self.processings:
        #     signal = processing(signal)

        spectrum, frequencies = tofrequencydomain(signal,sample_rate)
        bin_stats, bin_edges, binnumber = binned_statistic(frequencies,spectrum,statistic=log_rms,bins=self.bins)
        freq_data = (20*np.log10(bin_stats/self.reference_pressure)).T
        return freq_data
    
