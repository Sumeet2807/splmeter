import numpy as np
import copy

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
    
    def copy(self):
        return copy.deepcopy(self)

    def init(self,*args,**kwargs):
        pass


    def from_array(self,arr,fs):
        self.amplitude = np.array(arr)
        self.fs = fs
        op = Operation()
        op.name = 'Origin'
        op.parameters['Signal Type'] = self.type
        op.parameters['Signal Length(s)'] = self.amplitude.shape[-1]/self.fs
        op.parameters['Sample Frequency'] = self.fs
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

    def print_ops(self):
        
        for op in self.get_ops():
            print(op.name,op.parameters)

    
    def get_ops(self):
        ops_copy = self.ops.copy()
        op = Operation()
        op.name = 'End'
        op.parameters['Signal Type'] = self.type
        op.parameters['Signal Length(s)'] = self.amplitude.shape[-1]/self.fs
        op.parameters['Sample Frequency'] = self.fs
        ops_copy.append(op)
        return ops_copy




class BaseModule():

    def __init__(self,*args,**kwargs):
        self.name = 'Module'
        self.supported_signal_types = []
        self.parameters = {}
        return self.init(*args,**kwargs)


    def __call__(self,signal:BaseSignal):
        if not self.__signal_type_is_supported__(signal):
            raise Exception('Unsupported signal type. Supported signal types - %s' % (str(self.supported_signal_types)))
        signal = signal.copy()
        signal = self.process(signal)
        self.__register_to_signal__(signal)
        return signal
    

    def __register_to_signal__(self, signal):
        op = Operation()        
        op.name = self.name
        op.parameters = self.parameters
        signal.register_ops(op)
        
    def __signal_type_is_supported__(self,signal):
        if len(self.supported_signal_types):
            for signal_type in self.supported_signal_types:
                if isinstance(signal,signal_type):
                    return True                
            return False
        return True
    
    def register_supported_signal_type(self,signal_type):
        self.supported_signal_types.append(signal_type)
    
    def init(self,*args,**kwargs):
        pass

    def process(self,signal:BaseSignal):
        #override
        return signal
