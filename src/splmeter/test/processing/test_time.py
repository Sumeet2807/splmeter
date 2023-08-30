import numpy as np
from splmeter.base import BaseModule, BaseSignal
from splmeter.signal import SoundLevel,SoundPressure
from splmeter.processing.time import TimeWeight


class Test_time_weighting():


    def _get_4khz_step_signal(self,dur):
        freq = 4000
        fs = 48000
        noise_arr = np.zeros((fs*dur),dtype=np.int32)
        noise_arr[:int(fs*dur/2)] = np.cos((2*np.pi*freq)*(np.arange(0,fs*dur/2)/48000))
        return noise_arr, fs

    def test_4khz_response_fast(self):
        dur = 20
        noise_arr,fs = self._get_4khz_step_signal(dur)
        sig_noise = SoundPressure().from_array(noise_arr,fs)
        tw = TimeWeight(5,1,'Fast')
        sig_noise_tw = tw(sig_noise).amplitude
        delta = 0
        start = int(np.ceil(dur/2))
        for i in range(0,2):
            delta += (sig_noise_tw[start+i] - sig_noise_tw[start+i+1])
        assert delta/2 >= 25


    def test_4khz_response_slow(self):
        dur = 20
        noise_arr,fs = self._get_4khz_step_signal(dur)
        sig_noise = SoundPressure().from_array(noise_arr,fs)
        tw = TimeWeight(5,1,'Slow')
        sig_noise_tw = tw(sig_noise).amplitude
        delta = 0
        start = int(np.ceil(dur/2))
        for i in range(0,2):
            delta += (sig_noise_tw[start+i] - sig_noise_tw[start+i+1])
        assert (delta/2 >= 3.4 and delta/2 <= 5.3)



