from splmeter.base import BaseSignal


class SoundPressure(BaseSignal):
    def init(self):
        self.type = 'Pressure(Pa)/Volts(V)'
        self.unit = 'Pa/V'


class SoundLevel(BaseSignal):
    def init(self):        
        self.type = 'Level(dB)'
        self.unit = 'dB'

    
        