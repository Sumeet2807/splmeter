import numpy as np
from splmeter.base import BaseModule
from splmeter.signal import SoundLevel,SoundPressure

def resample(sig_arr,input_fs,output_fs):
    """Resamples a time domain signal

    Args:
        sig_arr (array): amplitude array
        input_fs (int): input sample rate
        output_fs (int): output sample rate

    Returns:
        _type_: resampled amplitude array, new sample rate
    """
    dur = sig_arr.shape[0]/input_fs
    n_output_samples = int(output_fs*dur)
    sample_times = np.arange(0,n_output_samples)/n_output_samples
    sample_indices = np.floor(sample_times*sig_arr.shape[0]).astype(np.int64)
    sig_arr = np.take(sig_arr,sample_indices)
    return sig_arr, output_fs


class VoltToSPL(BaseModule):
    """adjusts the signal for mic sensitivity
    """
    def init(self,mic_sensitivity):
        """init

        Args:
            mic_sensitivity (float): mic sensitivity to use
        """
        self.ms = mic_sensitivity
        self.name = 'Voltage to SPL'
        self.parameters['Mic Sensitivity'] = self.ms
        self.register_supported_signal_type(SoundPressure)
    def process(self,signal):
        """process

        Args:
            signal (SoundPressure): Signal instance

        Returns:
            SoundPressure: signal instance
        """
        signal.amplitude = signal.amplitude/self.ms
        return signal
    

class Resampler(BaseModule):
    """Resamples the input
    """
    def init(self,fs):
        """init

        Args:
            fs (int): new sample rate
        """
        self.new_fs = fs
        self.name = 'Resampler'
        self.parameters['Sample rate'] = self.new_fs
        

    def process(self, signal):
        """_summary_

        Args:
            signal (BaseSignal): Signal instance

        Returns:
            BaseSignal: Signal instance
        """
        new_signal = signal
        new_sig_arr,fs = resample(new_signal.amplitude,new_signal.fs,self.new_fs)
        new_signal.amplitude = new_sig_arr
        new_signal.fs = fs
        return new_signal
    

class TimeWeight(BaseModule):
    """Applies time weighting to a signal
    """
    def init(self,integration_window,output_resolution=1, type='Fast',timeconstant=0.125,start_time=0,max_input_fs=1000,reference_pressure=2e-5):        
        """Init

        Args:
            integration_window (float): window size to consider for looking into the past
            output_resolution (int, optional): Output will be calculated every n seconds. Defaults to 1.
            max_input_fs (int, optional): Resample the input to this frequency if input has a higher sample rate. Helps with performance. Defaults to 1000.
            reference_pressure (float, optional): Reference pressure for calculating decibel levels. Defaults to 2.0e-5.
            type (char): weighting type. Must be in [Fast, Slow, Custom]
            timeconstant(flaot): if type is Custom, specify the custom time-constant here

        """
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
        self.output_resolution = output_resolution
        self.max_input_fs = max_input_fs
        self.start_time = start_time
        self.name = 'Time Weighting'
        self.parameters['Weighting type'] = type
        self.parameters['Timeconstant'] = self.timeconstant
        self.parameters['Integration Window(s)'] = self.integration_window
        self.parameters['Compute every n seconds'] = self.output_resolution
        self.parameters['Max input sampling rate'] = max_input_fs
        self.parameters['Reference Pressure'] = self.rp
        self.register_supported_signal_type(SoundPressure)

    def process(self,signal):
        """_summary_

        Args:
            signal (SoundPressure): SoundPressure

        Returns:
            SoundLevel: SoundLevel
        """

        self.output_resolution = max(self.output_resolution, 1/signal.fs)
        
        if self.max_input_fs < signal.fs:
            resampler = Resampler(self.max_input_fs)
            signal = resampler(signal) 
        input_fs = signal.fs
        sig_arr = signal.amplitude


        integration_window_index_size = int(input_fs*self.integration_window)
        integration_time_index_size = int(input_fs*self.output_resolution)
        if integration_time_index_size <= 0:
            integration_time_index_size = 1
        start_index = int(self.start_time*input_fs)
        buffer = int(max(0,(integration_window_index_size - start_index)))
        start_index += buffer

        sig_arr=np.concatenate([np.array([0]*buffer),sig_arr],axis=0)
        # if start_index >= signal.shape[0]:
        #     raise Exception('Not enough samples in signal for the specified sample rate, integration window & time')
        # print('generating indices')
        indices = [np.arange(x-integration_window_index_size,x) for x in range(start_index,sig_arr.shape[0],integration_time_index_size)]
        exponential_term = np.exp(-1*(np.arange(integration_window_index_size-1,-1,-1)/input_fs)/self.timeconstant)[np.newaxis,...]
        summation_array = np.take(np.square(sig_arr),indices)*exponential_term

        new_amplitude = 10*np.log10((np.sum(summation_array,axis=1)/input_fs)/(self.timeconstant*(self.rp**2)))

        new_signal = SoundLevel().from_signal(signal,new_amplitude,1/(max(self.output_resolution,(1/input_fs))))

        return new_signal




        
