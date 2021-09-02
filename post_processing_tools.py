# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 13:20:21 2021

@author: moke
"""

import matplotlib.pyplot as plt
import os 
import numpy as np
def correct_drift(file,graph=0):
    mat=np.loadtxt(file)
    mat=np.array(mat)
    x_array=mat[:,1]
    #normalize and correct drift
    mean_start=np.mean(x_array[1:10])
    mean_end=np.mean(x_array[-10:])
    diff=mean_start-mean_end
    diff_array=np.linspace(0,diff,x_array.size)
    corr_x_array=x_array+diff_array
    
    if graph:
        plt.ylabel('X')
        plt.xlabel("magnetic field")
        plt.plot(mat[:,2],x_array,label='X')
    
        plt.ylabel('X_corrected')
        plt.xlabel("magnetic field")
        plt.plot(mat[:,2],corr_x_array,label='corrected X')
        plt.legend()
    else:
        lift=0.5*(corr_x_array.max()+corr_x_array.min())
        norm_x_array=corr_x_array-lift
    
    
        return [corr_x_array, norm_x_array] 


def myhisto(file):
    y=correct_drift(file)[1]
    bins=50
    thresh=0.5
    heights, bins = np.histogram(y, bins=bins)
    lbins = bins[:-1]
    binw = bins[1] - bins[0]
    igt0, ilt0 = lbins > 0, lbins < 0
    thresh_y = []
    hthresh = thresh * heights.max()
    for half, dx, ax in zip((igt0, ilt0), (0.0, binw), (1.0, -1.0)):
        saturated = np.where(half & (heights > hthresh))
        # dx is 0 for the gt0 side and binwidth for the lt0 side
        thresh_y.append(ax * min(abs(lbins[saturated])) + dx)

# Average over all points outside the thresholds to get the saturations
    y_saturations = (y[y > thresh_y[0]].mean(), y[y < thresh_y[1]].mean())
"""return dict(avg_val=np.abs(y_saturations).mean(),
            xcoords=np.array([np.min(x), np.max(x)]),
            ycoords=np.array(y_saturations),
            indices=None,
            thresh_y=thresh_y)"""
myhisto(r'C:\Users\moke\Desktop\PolLux\tests\pythontests\shorttimeconstantnolens_average')