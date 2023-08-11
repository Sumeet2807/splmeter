class VoltToSPL():
    def __init__(self,mic_sensitivity):
        self.ms = mic_sensitivity

    def __call__(self,signal):
        return signal/self.ms