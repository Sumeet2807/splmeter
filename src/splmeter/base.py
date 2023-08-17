import numpy as np

class Operation():
    name = None
    parameters = {}


class BaseSignal():
    
    amplitude = None
    fs = None
    sigtype = 'base'
    unit = None
    ops = []

    def from_array(self,arr,fs):
        self.amplitude = np.array(arr)
        self.fs = fs
        return self

    def register_ops(self,op: Operation):
        self.ops.append(op)

    def from_signal(self, signal):
        self.amplitude = signal.amplitude
        self.fs = signal.fs
        self.ops = signal.ops
        return self



class BaseModule():
    name = 'Base Module'
    parameters = {}
    def __call__(self,signal:BaseSignal):

        signal = self.process(signal)
        op = Operation()        
        op.name = self.name
        op.parameters = self.parameters
        signal.register_ops(op)
        return signal
        

    def process(self,signal:BaseSignal):
        #override
        return signal