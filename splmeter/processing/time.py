import numpy as np
import copy
from splmeter.base import BaseModule, BaseSignal
from splmeter.signal import SoundLevel,SoundPressure

def resample(sig_arr,input_fs,output_fs):
        dur = sig_arr.shape[0]/input_fs
        n_output_samples = int(output_fs*dur)
        sample_times = np.arange(0,n_output_samples)/n_output_samples
        sample_indices = np.floor(sample_times*sig_arr.shape[0]).astype(np.int64)
        sig_arr = np.take(sig_arr,sample_indices)
        return sig_arr, output_fs


class VoltToSPL(BaseModule):
    def init(self,mic_sensitivity):
        self.ms = mic_sensitivity
        self.name = 'Voltage to SPL'
        self.parameters['Mic Sensitivity'] = self.ms
        self.register_supported_signal_type(SoundPressure)
    def process(self,signal):
        signal.amplitude = signal.amplitude/self.ms
        return signal
    

class Resampler(BaseModule):
    def init(self,fs):
        self.new_fs = fs
        self.name = 'Resampler'
        self.parameters['Sample rate'] = self.new_fs
        

    def process(self, signal):
        new_signal = signal
        new_sig_arr,fs = resample(new_signal.amplitude,new_signal.fs,self.new_fs)
        new_signal.amplitude = new_sig_arr
        new_signal.fs = fs
        return new_signal
    

class TimeWeight(BaseModule):
    def init(self,integration_window,integration_time=1,type='Fast',timeconstant=0.125,reference_pressure=2e-5):
        if type == 'Fast':
            self.timeconstant = 0.125
        elif type == 'Slow':
            self.timeconstant = 1
        elif type == 'Custom':
            self.timeconstant = timeconstant
        else:
            raise Exception('Unsupported type for time weighting')
        
        self.rp = reference_pressure
        self.integration_window = integration_window
        self.integration_time = integration_time

        self.name = 'Time Weighting'
        self.parameters['Weighting type'] = type
        self.parameters['Timeconstant'] = self.timeconstant
        self.parameters['Integration Window(s)'] = self.integration_window
        self.parameters['Compute every n seconds'] = self.integration_time
        self.parameters['Reference Pressure'] = self.rp
        self.register_supported_signal_type(SoundPressure)

    def process(self,signal):
        integration_window_index_size = int(signal.fs*self.integration_window)
        integration_time_index_size = int(signal.fs*self.integration_time)
        if integration_time_index_size <= 0:
            integration_time_index_size = 1
        start_index = integration_window_index_size

        
        temp_amplitude =np.concatenate([np.array([0]*integration_window_index_size),signal.amplitude],axis=0)
        # if start_index >= signal.shape[0]:
        #     raise Exception('Not enough samples in signal for the specified sample rate, integration window & time')
        # print('generating indices')
        indices = [np.arange(x-integration_window_index_size,x) for x in range(start_index,temp_amplitude.shape[0],integration_time_index_size)]
        exponential_term = np.exp(-1*(np.arange(integration_window_index_size-1,-1,-1)/signal.fs)/self.timeconstant)[np.newaxis,...]
        summation_array = np.take(np.square(temp_amplitude),indices)*exponential_term

        new_amplitude = 10*np.log10((np.sum(summation_array,axis=1)/signal.fs)/(self.timeconstant*(self.rp**2)))

        new_signal = SoundLevel().from_signal(signal,new_amplitude,1/(max(self.integration_time,(1/signal.fs))))

        return new_signal




        
