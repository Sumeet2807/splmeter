import numpy as np
from scipy.signal import zpk2tf,lfilter, bilinear 
from numpy import pi, polymul
from numpy import pi
from scipy.signal import zpk2tf, zpk2sos, freqs, sosfilt
from splmeter.base import BaseModule, BaseSignal
from splmeter.signal import SoundPressure, SoundLevel
import numpy as np


def _relative_degree(z, p):
    """
    Return relative degree of transfer function from zeros and poles
    """
    degree = len(p) - len(z)
    if degree < 0:
        raise ValueError("Improper transfer function. "
                         "Must have at least as many poles as zeros.")
    else:
        return degree
def _zpkbilinear(z, p, k, fs):
    
    z = np.atleast_1d(z)
    p = np.atleast_1d(p)

    degree = _relative_degree(z, p)

    fs2 = 2.0*fs

    # Bilinear transform the poles and zeros
    z_z = (fs2 + z) / (fs2 - z)
    p_z = (fs2 + p) / (fs2 - p)

    # Any zeros that were at infinity get moved to the Nyquist frequency
    z_z = np.append(z_z, -np.ones(degree))

    # Compensate for gain change
    k_z = k * np.real(np.prod(fs2 - z) / np.prod(fs2 - p))

    return z_z, p_z, k_z




__all__ = ['ABC_weighting', 'A_weighting', 'A_weight']


def ABC_weighting(curve):
   
    if curve not in 'ABC':
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
        p = [-0.062*pi*20.598997057568145,-0.062*pi*20.598997057568145,
         -0.062*pi*12194.21714799801,-0.062*pi*12194.21714799801]
        
        
        
        
    b, a = zpk2tf(z, p, k)
    k /= abs(freqs(b, a, [2*pi*1000])[1][0])
    
    return np.array(z), np.array(p), k
    
        



def A_weighting(fs, output='ba'):
   
    z, p, k = ABC_weighting('A')

    # Use the bilinear transformation to get the digital filter.
    z_d, p_d, k_d = _zpkbilinear(z, p, k, fs)

    if output == 'zpk':
        return z_d, p_d, k_d
    elif output in {'ba', 'tf'}:
        return zpk2tf(z_d, p_d, k_d)
    elif output == 'sos':
        return zpk2sos(z_d, p_d, k_d)
    else:
        raise ValueError("'%s' is not a valid output form." % output)
        
def C_weighting(fs, output='ba'):
    z, p, k = ABC_weighting('C')

    # Use the bilinear transformation to get the digital filter.
    z_d, p_d, k_d = _zpkbilinear(z, p, k, fs)

    if output == 'zpk':
        return z_d, p_d, k_d
    
    elif output in {'ba', 'tf'}:
        return zpk2tf(z_d, p_d, k_d)
    elif output == 'sos':
        return zpk2sos(z_d, p_d, k_d)
    else:
        raise ValueError("'%s' is not a valid output form." % output)
    


class FrequencyWeight(BaseModule):
    def init(self,weighting_type='A'):
        if weighting_type == 'A':
            self.weight_fn = A_weighting
        elif weighting_type == 'C':
            self.weight_fn = C_weighting
        else:
            raise Exception('Unsupported weighting type')
        self.name = 'Frequency Weighting'
        self.parameters['Weighting Type'] = weighting_type

    def process(self,signal):
        sos = self.weight_fn(signal.fs,output='sos')
        signal.amplitude = sosfilt(sos, signal.amplitude)
        return signal