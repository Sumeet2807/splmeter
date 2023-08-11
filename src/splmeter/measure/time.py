import numpy as np


class Leq():

    def __init__(self, integration_window, integration_time, reference_pressure = 2.0e-5):
        self.integration_window = integration_window
        self.integration_time = integration_time
        self.rp = reference_pressure

    def __call__(self,signal,sample_rate):

        integration_window_index_size = sample_rate*self.integration_window
        integration_time_index_size = sample_rate*self.integration_time
        start_index = integration_window_index_size
        if start_index >= signal.shape[0]:
            raise Exception('Not enough samples in signal for the specified sample rate, integration window & time')
        print('generating indices')
        indices = [np.arange(x-integration_window_index_size,x) for x in range(start_index,signal.shape[0],integration_time_index_size)]
        print('generated indices')
        summation_array = np.take(np.square(signal),indices)

        return 10*np.log10(np.sum(summation_array,axis=1)/(integration_window_index_size*(self.rp**2)))