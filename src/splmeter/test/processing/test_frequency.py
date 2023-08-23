from splmeter.processing.frequency import FrequencyWeight
from splmeter.measure.frequency import OneThirdOctaveBinCentral
from splmeter.test.utils import get_tolerance_dict_from_csv
from splmeter.signal import SoundPressure,SoundLevel
from splmeter.measure.frequency import OneThirdOctave 
from splmeter.processing.frequency import FrequencyWeight
from splmeter.processing.time import VoltToSPL, Resampler, TimeWeight
import numpy as np


_TOLERANCE_FILE_NAME_ = 'C:/Users/Sumeet/Desktop/Projects/splmeter/src/splmeter/test/data/tol.csv'


class Test_frequency_weighting():
    def _weighting_test(self,type='A',iec_class='class1'):

        tolerance_dict = get_tolerance_dict_from_csv(_TOLERANCE_FILE_NAME_)

        fs = 48000
        sig_arr = None
        for freq in OneThirdOctaveBinCentral:
            if sig_arr is None:
                sig_arr = np.sin((2*np.pi*freq)*(np.arange(0,fs)/48000))
                continue
            sig_arr += np.sin((2*np.pi*freq)*(np.arange(0,fs)/48000))

        sig = SoundPressure().from_array(0.5*sig_arr,fs)
        oto = OneThirdOctave()
        fw = FrequencyWeight(type)
        sig_fw = fw(sig)
        sig_fw_o = oto(sig_fw)
        sig_o = oto(sig)
        residuals = sig_fw_o.amplitude - sig_o.amplitude
        for i,freq in enumerate(OneThirdOctaveBinCentral):
            if float(freq) in tolerance_dict:
                tolerance = tolerance_dict[float(freq)]
                benchmark = tolerance[type]
                diff = residuals[i]-benchmark
                assert  diff >= tolerance[iec_class][0] and diff <= tolerance[iec_class][1]

    def test_A_weighting(self):
        self._weighting_test('A','class1')
                    

