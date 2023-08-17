import numpy as np



class VoltToSPL():
    def __init__(self,mic_sensitivity):
        self.ms = mic_sensitivity

    def __call__(self,signal):
        return signal/self.ms
    

class Resampler():
    def __init__(self,new_fs):
        self.new_fs = new_fs
        

    def __call__(self, signal, fs):
        # if fs < self.new_fs:
        #     raise Exception('new sample rate cannot be higher than source sample rate')
        sample_times = np.arange(0,self.new_fs*int(signal.shape[0]/fs))/(self.new_fs*int(signal.shape[0]/fs))
        sample_indices = np.floor(sample_times*signal.shape[0]).astype(np.int64)
        return np.take(signal,sample_indices), self.new_fs
        


class TimeWeight():
    def __init__(self,integration_window,integration_time=0,type='Fast',timeconstant=0.125,reference_pressure=2e-5):
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

    def __call__(self,signal,fs):

        integration_window_index_size = int(fs*self.integration_window)
        integration_time_index_size = int(fs*self.integration_time)
        if integration_time_index_size <= 0:
            integration_time_index_size = 1
        start_index = integration_window_index_size

        
        signal=np.concatenate([np.array([0]*integration_window_index_size),signal],axis=0)
        # if start_index >= signal.shape[0]:
        #     raise Exception('Not enough samples in signal for the specified sample rate, integration window & time')
        # print('generating indices')
        indices = [np.arange(x-integration_window_index_size,x) for x in range(start_index,signal.shape[0],integration_time_index_size)]
        exponential_term = np.exp(-1*(np.arange(integration_window_index_size-1,-1,-1)/fs)/self.timeconstant)[np.newaxis,...]
        # print('generated indices')
        summation_array = np.take(np.square(signal),indices)*exponential_term


        return 10*np.log10((np.sum(summation_array,axis=1)/fs)/(self.timeconstant*(self.rp**2)))
        # return summation_array




        
