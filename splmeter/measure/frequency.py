from scipy.fft import fft, fftfreq
from scipy.stats import binned_statistic
import numpy as np
from splmeter.base import BaseModule
from splmeter.signal import SoundPressure, SoundLevel

def tofrequencydomain(signal,fs):
    """Converts a time domain signal to frequency domain using FFT

    Args:
        signal (Array): Sound pressure signal amplitude array to be processed
        fs (integer): Sample rate of the signal

    Returns:
        array, array: amplitude values per frequency, list of frequencies
    """
    spectrum = []

    for a in range(fs,signal.shape[0]+1,fs):
            
        b = a - fs
        yf = fft(signal[b:a])
        N = fs
        yf = 2.0/N * np.abs(yf[0:N//2])

        spectrum.append(yf)
    
    T = 1/fs
    frequencies = fftfreq(fs, T)[:fs//2]
    return np.array(spectrum),frequencies

def rss(data):
    """Derives root of sum of squares of values in an array

    Args:
        data (array): float array to be root sum of squares
    """
    return(np.sqrt(np.sum(np.square(data))))


class OneThirdOctave(BaseModule):
    """Derives one third octave bands from sound pressure signals

    """

    def init(self,reference_pressure = 2.0e-5):
        """Initialization

        Args:
            reference_pressure (float, optional): reference pressure for calculation of decibels. Defaults to 2.0e-5.
        """
        self.name = 'One-Third Octave'
        self.parameters['Reference Pressure'] = reference_pressure
        self.reference_pressure = reference_pressure
        self.bins = OneThirdOctaveBins        
        self.bin_names = OneThirdOctaveBinCentral
        self.register_supported_signal_type(SoundPressure)


    def process(self, signal):
        """_summary_

        Args:
            signal (SoundPressure): Sound pressure signal instance

        Raises:
            Exception: Unsupported signal type

        Returns:
            SoundLevel: Sound pressure level instance
        """
        # for processing in self.processings:
        #     signal = processing(signal)
        if not isinstance(signal, SoundPressure):
             raise Exception('Unsupported signal type. Supported type - splmeter.signal.SoundPressure')
        
        spectrum, frequencies = tofrequencydomain(signal.amplitude,signal.fs)
        bin_stats, bin_edges, binnumber = binned_statistic(frequencies,spectrum,statistic=rss,bins=self.bins)
        freq_data = (20*np.log10(bin_stats/self.reference_pressure)).T
        new_signal =  SoundLevel().from_signal(signal,freq_data,1)
        return new_signal
    



OneThirdOctaveBins = [
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

OneThirdOctaveBinCentral = [
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