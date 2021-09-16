# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 13:20:21 2021

@author: moke
"""

import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import os 
import numpy as np
import pandas as pd
class myloop:
    
    def __init__(self,file):
        self.file = file
        mat=np.array(np.loadtxt(self.file))
        self.aux_1=mat[:,0]
        self.mag_field=self.aux_1*1600
        self.x_array=mat[:,1]
        self.y_array=mat[:,2]
        self.r_array=mat[:,3]
        self.norm_x_array=self.normalize()
        
        
    def correct_drift(self, graph):
        from matplotlib import pyplot as plt
        #mat=np.loadtxt(file)
        #mat=np.array(mat)
        #x_array=mat[:,1]
        mean_start=np.mean(self.x_array[1:10])
        mean_end=np.mean(self.x_array[-10:])
        diff=mean_start-mean_end
        diff_array=np.linspace(0,diff,self.x_array.size)
        corr_x_array=self.x_array+diff_array#x with drift only corrected
        lift=0.5*(corr_x_array.max()+corr_x_array.min())
        norm_x_array=corr_x_array-lift
        N=len(np.array(self.aux_1))
        if graph == 0:
            plt.ylabel('X')
            plt.xlabel("magnetic field")
            plt.plot(self.mag_field,self.x_array,label='X')
            plt.ylabel('X_corrected')
            plt.xlabel("magnetic field")
            plt.plot(self.mag_field,corr_x_array,label='corrected X')
            plt.legend()
            plt.show()
        if graph == 1:
            plt.ylabel('Y')
            plt.xlabel("magnetic field")
            plt.plot(self.mag_field,self.y_array,label='Y')
            plt.show()
        if graph == 2:
            return [corr_x_array, norm_x_array]
        else:
            plt.ylabel('normalized and corrected X')
            plt.xlabel("magnetic field")
            plt.plot(self.mag_field,norm_x_array,label='X')
            y_sat=self.myhisto(1)
            plt.axhline(y=y_sat[0],xmin=self.aux_1[0], xmax=0)
            plt.axhline(y=y_sat[1],xmin=0, xmax=-self.aux_1[N//2])
            plt.show()
    def normalize(self):
        mean_start=np.mean(self.x_array[1:10])
        mean_end=np.mean(self.x_array[-10:])
        diff=mean_start-mean_end
        diff_array=np.linspace(0,diff,self.x_array.size)
        corr_x_array=self.x_array+diff_array#x with drift only corrected
        lift=0.5*(corr_x_array.max()+corr_x_array.min())
        norm_x_array=corr_x_array-lift
        return norm_x_array
    def myhisto(self, outp):
        y= self.norm_x_array
        N = len(y)
        ych0, ych1 = y[:N//2], y[N//2:]
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
        y_indices_0= list(np.argmin(abs(y-thresh_y[0])) for y in  (ych0, ych1))
        y_indices_1= list(np.argmin(abs(y-thresh_y[1])) for y in  (ych0, ych1))
# Average over all points outside the thresholds to get the saturations
        y_saturations = (y[y > thresh_y[0]].mean(), y[y < thresh_y[1]].mean())
        y_saturation2 = (y[y > thresh_y[0]], y[y < thresh_y[1]])
        if outp:
            return y_saturations
        else:
            return y_saturation2
    def get_coercivity(self):
        h, x = np.array(self.aux_1), np.array(self.correct_drift(0)[1])
        N = len(x)
        xch0, xch1 = x[:N//2], x[N//2:]
        hc_indices = list(np.argmin(np.abs(x)) for x in (xch0, xch1))
        hc_indices[1] += N//2
        coercivity=(abs(h[hc_indices[0]])+abs(h[hc_indices[1]]))/2
        return coercivity
    
    def get_variance(self, n):
        N=len(self.norm_x_array)
        x_f=self.norm_x_array[:N//2]
        x_bac=self.norm_x_array[N//2:]
        mov_ave_f=pd.Series(x_f).rolling(window=n).mean().iloc[n-1:].values
        mov_ave_b=pd.Series(x_bac).rolling(window=n).mean().iloc[n-1:].values
        
    def get_snr(self):
        y=self.myhisto(0)
        var=np.var(y[0])+np.var(y[1])
        signal=self.myhisto(1)[1]-self.myhisto(1)[0]
        snr= signal^2/var
        snr_db=10*np.log10(snr)
        return snr, snr_db
        
a=myloop(r'C:\Users\moke\Desktop\PolLux\tests\pythontests\5timecon6dblownoise_average')
a.correct_drift(1)
"""return dict(avg_val=np.abs(y_saturations).mean(),
            xcoords=np.array([np.min(x), np.max(x)]),
            ycoords=np.array(y_saturations),
            indices=None,
            thresh_y=thresh_y)"""
