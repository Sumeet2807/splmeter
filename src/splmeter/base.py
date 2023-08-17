import numpy as np

class Operation():
    def __init__(self):
        self.name = None
        self.parameters = {}


class BaseSignal():

    def __init__(self,*args,**kwargs):
    
        self.amplitude = None
        self.fs = None
        self.type = 'base'
        self.unit = None
        self.ops = []
        return self.init(*args,**kwargs)

    def init(self,*args,**kwargs):
        pass


    def from_array(self,arr,fs):
        self.amplitude = np.array(arr)
        self.fs = fs
        op = Operation()
        op.name = 'Origin'
        op.parameters['Signal Type'] = self.type
        op.parameters['Signal Length(s)'] = self.amplitude.shape[0]/self.fs
        op.parameters['Sample Frequency'] = fs
        self.register_ops(op)
        return self

    def register_ops(self,op: Operation):
        self.ops.append(op)

    def from_signal(self, signal, amplitude=None,fs=None):
        if amplitude is None:
            self.amplitude = signal.amplitude
        else:
            self.amplitude = amplitude
        if fs is None:
            self.fs = signal.fs
        else:
            self.fs = fs
        self.ops = signal.ops
        return self



class BaseModule():

    def __init__(self,*args,**kwargs):
        self.name = 'Module'
        self.parameters = {}
        return self.init(*args,**kwargs)


    def __call__(self,signal:BaseSignal):

        signal = self.process(signal)
        self.__register_to_signal__(signal)
        return signal
        

    def init(self,*args,**kwargs):
        pass

    def process(self,signal:BaseSignal):
        #override
        return signal
    

    def __register_to_signal__(self, signal):
        op = Operation()        
        op.name = self.name
        op.parameters = self.parameters
        signal.register_ops(op)
