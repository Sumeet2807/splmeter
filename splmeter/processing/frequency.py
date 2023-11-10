import numpy as np
from scipy.signal import zpk2tf,bilinear_zpk 
from numpy import pi
from scipy.signal import zpk2tf, zpk2sos, freqs, sosfilt
from splmeter.base import BaseModule
from splmeter.signal import SoundPressure
import numpy as np


def AC_weighting(curve):
    """_summary_

    Args:
        curve (char): type of weighting

    Raises:
        ValueError: Unsupported weighting curve

    Returns:
        _type_: curve filter transfer function
    """
   
    if curve not in 'AC':
        raise ValueError('Curve type not understood')

    z = [0, 0]
    k = 1

    if curve == 'A':
       
        p = [-2*pi*20.598997057568145,
         -2*pi*20.598997057568145,
         -2*pi*12194.21714799801,
         -2*pi*12194.21714799801]
        p.append(-2*pi*107.65264864304628)
        p.append(-2*pi*737.8622307362899)
        z.append(0)
        z.append(0)

    elif curve == 'C':
        
        p = [-2*pi*20.598997057568145,
         -2*pi*20.598997057568145,
         -2*pi*12194.21714799801,
         -2*pi*12194.21714799801]
        
        
    b, a = zpk2tf(z, p, k)
    k /= abs(freqs(b, a, [2*pi*1000])[1][0])
    
    return np.array(z), np.array(p), k
    
        



def A_weighting(fs, output='ba'):
   
    z, p, k = AC_weighting('A')

    # Use the bilinear transformation to get the digital filter.
    # z_d, p_d, k_d = _zpkbilinear(z, p, k, fs)
    z_d, p_d, k_d = bilinear_zpk(z, p, k, fs)

    if output == 'zpk':
        return z_d, p_d, k_d
    elif output in {'ba', 'tf'}:
        return zpk2tf(z_d, p_d, k_d)
    elif output == 'sos':
        return zpk2sos(z_d, p_d, k_d)
    else:
        raise ValueError("'%s' is not a valid output form." % output)
        
def C_weighting(fs, output='ba'):
    z, p, k = AC_weighting('C')

    # Use the bilinear transformation to get the digital filter.
    # z_d, p_d, k_d = _zpkbilinear(z, p, k, fs)
    z_d, p_d, k_d = bilinear_zpk(z, p, k, fs)

    if output == 'zpk':
        return z_d, p_d, k_d
    
    elif output in {'ba', 'tf'}:
        return zpk2tf(z_d, p_d, k_d)
    elif output == 'sos':
        return zpk2sos(z_d, p_d, k_d)
    else:
        raise ValueError("'%s' is not a valid output form." % output)
    


class FrequencyWeight(BaseModule):
    """Derives frequency weighted sound pressure signal
    """
    def init(self,weighting_type='A',start_time=0):
        """_summary_

        Args:
            weighting_type (str, optional): Weighting type to use. Must be in [A,C]. Defaults to 'A'.

        Raises:
            Exception: Unsupported weighting type
        """
        if weighting_type == 'A':
            self.weight_fn = A_weighting
        elif weighting_type == 'C':
            self.weight_fn = C_weighting
        else:
            raise Exception('Unsupported weighting type')
        self.name = 'Frequency Weighting'
        self.parameters['Weighting Type'] = weighting_type
        self.register_supported_signal_type(SoundPressure)
        self.start_time = start_time

    def process(self,signal):
        """_summary_

        Args:
            signal (SoundPressure): Sound Pressure signal instance

        Returns:
            SoundPressure: Sound Pressure signal instance
        """
        start_index = int(self.start_time*signal.fs)
        sos = self.weight_fn(signal.fs,output='sos')
        amplitude = sosfilt(sos, signal.amplitude[start_index:])
        new_signal =  SoundPressure().from_signal(signal,amplitude,signal.fs)
        return new_signal