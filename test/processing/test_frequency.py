from splmeter.processing.frequency import FrequencyWeight
from splmeter.measure.frequency import OneThirdOctaveBinCentral
from test.utils import get_tolerance_dict_from_csv
from splmeter.signal import SoundPressure
from splmeter.measure.frequency import OneThirdOctave 
import numpy as np





class Test_frequency_weighting():

    # _TOLERANCE_FILE_RELATIVE_PATH_ = 'C:/Users/Sumeet/Desktop/Projects/splmeter/src/splmeter/test/data/frequency_weigting_tolerance_AC.csv'
    _TOLERANCE_FILE_RELATIVE_PATH_ = 'data/frequency_weigting_tolerance_AC.csv'   #path is relative to test folder

    def _get_white_noise(self):
        fs = 48000
        noise_arr = None
        for freq in OneThirdOctaveBinCentral:
            if noise_arr is None:
                noise_arr = np.sin((2*np.pi*int(freq))*(np.arange(0,fs)/48000))
                continue
            noise_arr += np.sin((2*np.pi*int(freq))*(np.arange(0,fs)/48000))
        return noise_arr, fs

    def _weighting_test(self,type='A',iec_class='class1'):

        tolerance_dict = get_tolerance_dict_from_csv(self._TOLERANCE_FILE_RELATIVE_PATH_)
        self.noise_arr, self.noise_fs = self._get_white_noise()
        
        sig = SoundPressure().from_array(self.noise_arr, self.noise_fs)
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

    def test_A_weighting_class_1(self):
        self._weighting_test('A','class1')

    def test_C_weighting_class_1(self):
        self._weighting_test('C','class1')

    def test_A_weighting_class_2(self):
        self._weighting_test('A','class2')

    def test_C_weighting_class_2(self):
        self._weighting_test('C','class2')


