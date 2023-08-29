from splmeter.measure.frequency import OneThirdOctaveBinCentral
from splmeter.signal import SoundPressure
from splmeter.measure.frequency import OneThirdOctave 
import numpy as np



class Test_octave():
    _REFERENCE_PRESSURE = 2e-5
    def _get_random_noise(self,n_components=5):
        fs = 48000
        noise_arr = None
        random_multiplier = np.random.randint(1,1000)/10000
        random_indices = np.random.randint(0,len(OneThirdOctaveBinCentral),n_components,dtype=np.int32)
        selected_frequency = np.array(OneThirdOctaveBinCentral)[random_indices]
        noise_amp = np.zeros((len(OneThirdOctaveBinCentral)))
        for i, freq in enumerate(selected_frequency):
            noise_amp[random_indices[i]] += random_multiplier
            if noise_arr is None:
                noise_arr = random_multiplier*np.cos((2*np.pi*int(freq))*(np.arange(0,fs)/48000))
                continue
            noise_arr += random_multiplier*np.cos((2*np.pi*int(freq))*(np.arange(0,fs)/48000))
        noise_arr_db = 20*np.log10(noise_amp/self._REFERENCE_PRESSURE)
        return noise_arr, fs, np.clip(noise_arr_db,0,None)

    def _get_white_noise(self):
        fs = 48000
        noise_arr = None
        for freq in OneThirdOctaveBinCentral:
            if noise_arr is None:
                noise_arr = np.cos((2*np.pi*int(freq))*(np.arange(0,fs)/48000))
                continue
            noise_arr += np.cos((2*np.pi*int(freq))*(np.arange(0,fs)/48000))
        noise_arr_db = 20*np.log10(np.ones((len(OneThirdOctaveBinCentral)))/self._REFERENCE_PRESSURE)
        return noise_arr, fs, np.clip(noise_arr_db,0,None)
    

    def test_octave_white_noise_tolerance_1db(self):
        sig_arr,fs,sig_db = self._get_white_noise()
        sig = SoundPressure().from_array(sig_arr,fs)
        oto = OneThirdOctave(self._REFERENCE_PRESSURE)
        sig_o = np.clip(oto(sig).amplitude,0,None)
        assert np.max(np.abs(sig_o-sig_db[...,np.newaxis])) < 1

    def test_octave_random_noise_tolerance_1db(self):
        sig_arr,fs,sig_db = self._get_random_noise()
        sig = SoundPressure().from_array(sig_arr,fs)
        oto = OneThirdOctave(self._REFERENCE_PRESSURE)
        sig_o = np.clip(oto(sig).amplitude,0,None)
        assert np.max(np.abs(sig_o-sig_db[...,np.newaxis])) < 1
