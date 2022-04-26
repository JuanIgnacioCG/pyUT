'''
pyUT.py by Juan Ignacio Caballero

script to open an ultrasound volume by Napari library then compute:
 > alignment of the array in the depth (wave propagation direction).
 > compute attenuation as an operation between the peaks. 

So far only for IMDEAs UT
'''

import napari
import numpy as np
from scipy.signal import hilbert

import matplotlib.pyplot as plt
import Pred_asc as pasc
import Pred_tomo as ptom
from pathlib import Path
from PIL import Image
import os


def attenuation(A,A_0):
    return ((10 *  np.log10(np.divide(A, A_0, where=A_0 != 0)+0.0001)) *(-2))

def att_12(array, inter11, inter12, inter21, inter22):
    # Segmenting volume in first and second interface slices
    interfaz1 = array[:,:,inter11:inter12]
    interfaz2 = array[:,:,inter21:inter22]

    # Obtaining max
    inter1_peaks = np.amax(interfaz1, axis=2)
    inter2_peaks = np.amax(interfaz2, axis=2)

    # Applying formula of attenuation. Adding 0.0001 to avoid division by 0.
    return(attenuation(inter2_peaks, inter1_peaks+0.0001))

def envalign_byenv(envelope,ref_a,low_limit):
    '''
    Only for env. signals. It takes the envelope and align all the maximums at ref_a position.
    ref_a: x desired position to start all signals. It must be before all of them.
    low_limit: a minimum threshold to align a signal
    '''
    array1d = envelope
    align = np.zeros(len(envelope))
    pad = np.argmax(envelope) - ref_a
    if np.argmax(envelope)>low_limit:
        end = len(envelope[(pad-ref_a):(ref_a-pad)])+ref_a
        # print(align[ref_a:].shape, (pad-ref_a),(ref_a-pad),pad)
        align[ref_a:end] = envelope[(pad-ref_a):(ref_a-pad)]
        return align
    else:
        return align    
    
    
## OLD     
    # array1d = envelope
    # align = np.zeros(envelope.shape)
    # pad = np.argmax(envelope) - ref_a
    # if np.argmax(envelope)>low_limit:
    #     # end = len(envelope[pad:])
    #     align[ref_a:] = envelope[(pad-ref_a):(ref_a-pad)]
    #     return align
    # else:
    #     return align

if __name__ == "__main__":
    viewer = napari.Viewer()
    napari.run()