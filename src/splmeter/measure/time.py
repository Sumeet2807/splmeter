import numpy as np


class Leq():

    def __init__(self, integration_window, integration_time=1, reference_pressure = 2.0e-5):
        self.integration_window = integration_window
        self.integration_time = integration_time
        self.rp = reference_pressure

    def __call__(self,signal,sample_rate):

        integration_window_index_size = sample_rate*self.integration_window
        integration_time_index_size = sample_rate*self.integration_time
        if integration_time_index_size <= 0:
            integration_time_index_size = 1
        start_index = integration_window_index_size

        signal=np.concatenate([np.array([0]*integration_window_index_size),signal],axis=0)

        if start_index >= signal.shape[0]:
            raise Exception('Not enough samples in signal for the specified sample rate, integration window & time')
        indices = [np.arange(x-integration_window_index_size,x) for x in range(start_index,signal.shape[0],integration_time_index_size)]
        summation_array = np.take(np.square(signal),indices)

        return 10*np.log10(np.sum(summation_array,axis=1)/(integration_window_index_size*(self.rp**2)))
    



class Lmax():
     
    def __init__(self, compute_window, compute_time,reference_pressure = 2.0e-5):
        self.compute_window = compute_window
        self.compute_time = compute_time
        self.rp = reference_pressure

    
    def __call__(self,signal,sample_rate):

        compute_window_index_size = sample_rate*self.compute_window
        compute_time_index_size = sample_rate*self.compute_time
        if compute_time_index_size <= 0:
            compute_time_index_size = 1
        start_index = compute_window_index_size

        signal=np.concatenate([np.array([0]*compute_window_index_size),signal],axis=0)

        if start_index >= signal.shape[0]:
            raise Exception('Not enough samples in signal for the specified sample rate, compute window & time')
        
        # print('generating')        
        indices = [np.arange(x-compute_window_index_size,x) for x in range(start_index,signal.shape[0],compute_time_index_size)]
        # print('generated')
        compute_array = np.take(signal,indices)
        return np.max(compute_array,axis=1)


