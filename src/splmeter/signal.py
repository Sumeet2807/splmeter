from splmeter.base import BaseSignal


class SoundPressure(BaseSignal):
    def init(self):
        self.type = 'pressure(Pa)'
        self.unit = 'Pa'


class SoundLevel(BaseSignal):
    def init(self):        
        self.type = 'level(dB)'
        self.unit = 'dB'

    
        