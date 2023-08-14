import numpy as np

class VoltToSPL():
    def __init__(self,mic_sensitivity):
        self.ms = mic_sensitivity

    def __call__(self,signal):
        return signal/self.ms
    

class Resampler():
    def __init__(self,new_sample_rate):
        self.new_sample_rate = new_sample_rate
        

    def __call__(self, signal, sample_rate):
        # if sample_rate < self.new_sample_rate:
        #     raise Exception('new sample rate cannot be higher than source sample rate')
        sample_times = np.arange(0,self.new_sample_rate*int(signal.shape[0]/sample_rate))/(self.new_sample_rate*int(signal.shape[0]/sample_rate))
        sample_indices = np.floor(sample_times*signal.shape[0]).astype(np.int64)
        return np.take(signal,sample_indices), self.new_sample_rate
        


class TimeWeight():
    def __init__(self,integration_window,type='Fast',timeconstant=0.125,reference_pressure=2e-5):
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
        

    def __call__(self,signal,sample_rate):

        integration_window_index_size = sample_rate*self.integration_window
        # integration_time_index_size = sample_rate*self.integration_time
        signal=np.concatenate([np.array([0]*integration_window_index_size),signal],axis=0)
        start_index = integration_window_index_size
        # if start_index >= signal.shape[0]:
        #     raise Exception('Not enough samples in signal for the specified sample rate, integration window & time')
        # print('generating indices')
        indices = [np.arange(x-integration_window_index_size,x) for x in range(start_index,signal.shape[0])]
        exponential_term = np.exp(-1*np.arange(integration_window_index_size,0,-1)/self.timeconstant)[np.newaxis,...]
        # print('generated indices')
        summation_array = np.take(np.square(signal),indices)*exponential_term

        return 10*np.log10(np.sum(summation_array,axis=1)/(self.timeconstant*(self.rp**2)))
