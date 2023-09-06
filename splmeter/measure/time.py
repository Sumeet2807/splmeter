from splmeter.processing.time import Resampler
from splmeter.signal import SoundLevel,SoundPressure
from splmeter.base import BaseModule
import numpy as np

class Leq(BaseModule):

    def init(self, averaging_window, output_resolution=1, max_input_fs=1000, reference_pressure = 2.0e-5):
        self.averaging_window = averaging_window
        self.output_resolution = output_resolution
        self.rp = reference_pressure
        self.max_input_fs = max_input_fs
        self.name = 'Equivalent continuous sound level(Leq)'
        self.parameters['Averaging window/time'] = averaging_window
        self.parameters['Output resolution']=output_resolution
        self.parameters['Max input sampling rate'] = max_input_fs
        self.parameters['Reference Pressure'] = reference_pressure
        self.register_supported_signal_type(SoundPressure)

    def process(self,signal):
        
        self.output_resolution = max(self.output_resolution, 1/signal.fs)
        
        if self.max_input_fs < signal.fs:
            resampler = Resampler(self.max_input_fs)
            signal = resampler(signal)        
        
        input_fs = signal.fs
        sig_arr = signal.amplitude

        averaging_window_index_size = int(input_fs*self.averaging_window)
        averaging_window_step_size = int(input_fs*self.output_resolution)
        if averaging_window_step_size <= 0:
            averaging_window_step_size = 1
        start_index = averaging_window_index_size

        sig_arr=np.concatenate([np.array([0]*averaging_window_index_size),sig_arr],axis=0)

        if start_index >= sig_arr.shape[0]:
            raise Exception('Not enough samples in signal for the specified sample rate, integration window & time')
        indices = [np.arange(x-averaging_window_index_size,x) for x in range(start_index,sig_arr.shape[0],averaging_window_step_size)]
        summation_array = np.take(np.square(sig_arr),indices)
        new_sig_arr = 10*np.log10(np.sum(summation_array,axis=1)/(averaging_window_index_size*(self.rp**2)))
        new_signal = SoundLevel().from_signal(signal)
        new_signal.amplitude = new_sig_arr
        new_signal.fs = 1/self.output_resolution

        return new_signal
    



class Lmax(BaseModule):
     
    def init(self, compute_window, output_resolution=1):
        self.compute_window = compute_window
        self.output_resolution = output_resolution
        self.name = 'Maximum time-weighted sound level(Lmax)'
        self.parameters['Compute window/time'] = compute_window
        self.parameters['Output resolution'] = output_resolution
        self.register_supported_signal_type(SoundLevel)


    
    def process(self,signal):

        input_fs = signal.fs
        sig_arr = signal.amplitude
        compute_window_index_size = int(input_fs*self.compute_window)
        compute_window_step_size = int(input_fs*self.output_resolution)
        if compute_window_step_size <= 0:
            compute_window_step_size = 1
        start_index = compute_window_index_size

        sig_arr=np.concatenate([np.array([0]*compute_window_index_size),sig_arr],axis=0)

        if start_index >= sig_arr.shape[0]:
            raise Exception('Not enough samples in signal for the specified sample rate, compute window & time')
        
    
        indices = [np.arange(x-compute_window_index_size,x) for x in range(start_index,sig_arr.shape[0],compute_window_step_size)]
        compute_array = np.take(sig_arr,indices)
        new_sig_arr = np.max(compute_array,axis=1)
        new_signal = SoundLevel().from_signal(signal)
        new_signal.amplitude = new_sig_arr
        new_signal.fs = 1/self.output_resolution

        return new_signal


class Lpeak(BaseModule):
     
    def init(self, compute_window, output_resolution=1,reference_pressure = 2.0e-5):
        self.compute_window = compute_window
        self.output_resolution = output_resolution
        self.rp = reference_pressure
        self.name = 'Peak sound level(Lpeak)'
        self.parameters['Compute window/time'] = compute_window
        self.parameters['Output resolution'] = output_resolution
        self.parameters['Reference Pressure'] = reference_pressure
        self.register_supported_signal_type(SoundPressure)


    
    def process(self,signal):

        input_fs = signal.fs
        sig_arr = signal.amplitude
        compute_window_index_size = int(input_fs*self.compute_window)
        compute_window_step_size = int(input_fs*self.output_resolution)
        if compute_window_step_size <= 0:
            compute_window_step_size = 1
        start_index = compute_window_index_size

        sig_arr=np.concatenate([np.array([0]*compute_window_index_size),sig_arr],axis=0)

        if start_index >= sig_arr.shape[0]:
            raise Exception('Not enough samples in signal for the specified sample rate, compute window & time')
        
    
        indices = [np.arange(x-compute_window_index_size,x) for x in range(start_index,sig_arr.shape[0],compute_window_step_size)]
        compute_array = np.take(sig_arr,indices)
        new_sig_arr = 10*np.log10(np.square(np.max(compute_array,axis=1))/self.rp**2)
        new_signal = SoundLevel().from_signal(signal)
        new_signal.amplitude = new_sig_arr
        new_signal.fs = 1/self.output_resolution

        return new_signal
