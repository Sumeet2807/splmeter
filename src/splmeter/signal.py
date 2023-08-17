from splmeter.base import BaseSignal


class SoundPressure(BaseSignal):
    def __init__(self):
        super().__init__()
        self.sigtype = 'pressure'
        self.unit = 'Pa'


class SoundLevel(BaseSignal):
    def __init__(self):
        super().__init__()
        self.sigtype = 'level'
        self.unit = 'dB'

    
        