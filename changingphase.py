# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 16:31:12 2021

@author: moke
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import tkinter as tk
import numpy as np
import os
import time
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import qcodes as qc
import numpy as np
from time import sleep
from qcodes.instrument_drivers.stanford_research.SR830 import SR830
from qcodes.utils.dataset import doNd
from qcodes import load_or_create_experiment
from qcodes.instrument.base import Instrument
from qcodes.utils.validators import Numbers
from qcodes.tests.instrument_mocks import DummyInstrument, DummyInstrumentWithMeasurement


window = tk.Tk()
sr = SR830('lockin30', 'GPIB0::5::INSTR')


def main_function():
    "initialize"
    "read data"
    nos = int(entry_nos.get())
    noa = int(entry_noa.get())
    minfield = int(entry_minfield.get())
    maxfield = int(entry_maxfield.get())
    #kerref = entry_kerref.get()
    #kerrsup = entry_kerrsup.get()
    
    
    sample_name=entry_sample.get()
    filepath=entry_fpath.get()
    date_time=time.strftime("%Y%m%d-%H%M%S")
    date=time.strftime("%Y%m%d")
    timee=time.strftime("%H%M%S")
    
    
    #time_con=entry_tcon.get()
    #res=entry_res.get()
    #sen=entry_sen.get()
    #fslope=entry_fslope.get()
    
    
    "set it to sr830"
   # sr.time_constant(time_con)
   # sr.sensitivity(sen)
    #sr.filter_slope(fslope)
   # sr.reserve(res)
    
    
    "set it to minimal voltage"
    minvolt=minfield
    maxvolt=maxfield
    sr.phase(minvolt)
    "array of all the voltages"
    volt1=np.linspace(minvolt,maxvolt,nos)
    volt2=np.linspace(maxvolt,minvolt,nos)
    volt=np.concatenate((volt1,volt2),axis=None)
    average_X=np.zeros([volt.size,noa])
    average_Y=np.zeros([volt.size,noa])
    average_phase=np.zeros([volt.size,noa])
    for j in range(noa):
        results=np.zeros([volt.size,4])
        results[:,0]=volt
        for i in range(volt.size):
            cur_volt=volt[i]
            sr.phase.set(cur_volt)
            time.sleep(0.8)
            _=np.array(sr.snap('x','y','phase'))
            results[i,[0]]=sr.phase.get()
            results[i,[1,2,3]]=_
        print(sr.phase())
        average_X[:,j]=results[:,1]
        average_Y[:,j]=results[:,2]
        average_phase[:,j]=results[:,3]
    average_results=np.zeros([volt.size,4])
    average_results[:,0]=volt
    average_results[:,1]=np.mean(average_X,axis=1)
    average_results[:,2]=np.mean(average_Y,axis=1)
    average_results[:,3]=np.mean(average_phase,axis=1)
    #for n in range(volt.size):
        #if n == 0:
        #    with open(os.path.join(filepath, sample_name+date_time), 'w') as fp:
        #        fp.write("Date\t"+date+"\tTime\t"+timee)
                #linestowrite=["\nTime constant:", "Filter Slope:", "Sensitivity:", "Line filter:", "Reserve:", "Coupling:", "Ground:"]
                #for i in linestowrite:
                    #fp.write(i+"\t")
    fileName=os.path.join(filepath, sample_name+date_time)
    mat = np.matrix(average_results)
    #with open(fileName,'wb') as f:
     #   for line in mat:
      #      np.savetxt(f, line, fmt='%.2f')
    print(mat)


















frame1 = tk.Frame(master=window,bg='grey', width=1000, height=1500, padx= 30, pady=30)
frame2 = tk.Frame(master=window,bg='grey', height=500, padx= 30, pady= 30)
frame3 = tk.Frame(master=window,bg='grey', height=500, padx= 30, pady=5)
frame5 = tk.Frame(master=window,bg='grey', height=500, padx= 30, pady=10)

frame1.grid(row=0, sticky="ew")
frame2.grid(row=1, sticky="ew")
frame3.grid(row=2, sticky="ew")
frame5.grid(row=3, sticky="ew")

OPTIONS = [
"Jan",
"Feb",
"Mar"
]
#FRAME 1

VISA_label = tk.Label(master=frame1, text='VISA resource name')
nos_label = tk.Label(master=frame1, text="Number of steps")
noa_label = tk.Label(master=frame1, text='Number of averages')
minfield_label = tk.Label(master=frame1, text='Min magn field')
maxfield_label = tk.Label(master=frame1, text='Max magn field')

VISA_label.grid(row=0, column=1,pady= 5)
entry_VISA = tk.StringVar(frame1)
entry_VISA.set(OPTIONS[0]) # default value
w = tk.OptionMenu(frame1, entry_VISA, *OPTIONS)
w.grid(row=1, column=1,pady= 5)


entry_nos = tk.Entry(master=frame1, background="white")
entry_noa = tk.Entry(master=frame1, background="white")
entry_minfield = tk.Entry(master=frame1, background="white")
entry_maxfield = tk.Entry(master=frame1, background="white")


nos_label.grid(row=3, column=0)
noa_label.grid(row=3, column=3)
entry_nos.grid(row=4, column=0,pady= 3)
entry_noa.grid(row=4, column=3,pady= 3)

minfield_label.grid(row=6, column=0)
maxfield_label.grid(row=6, column=3)
entry_minfield.grid(row=7, column=0,  padx= 20)
entry_maxfield.grid(row=7, column=3,  padx= 10)

#FRAME 2
kerref_label = tk.Label(master=frame2, text='Kerr effect')
kerrsup_label = tk.Label(master=frame2, text="Kerr signal")

kerref_label.grid(row=0, column=0,pady= 5)
entry_kerref = tk.StringVar(frame1)
entry_kerref.set(OPTIONS[0]) # default value
w = tk.OptionMenu(frame2, entry_kerref, *OPTIONS)
w.grid(row=1, column=0,pady= 5)

kerrsup_label.grid(row=0, column=2,pady= 5,padx= 20)
entry_kerrsup = tk.StringVar(frame1)
entry_kerrsup.set(OPTIONS[0]) # default value
w = tk.OptionMenu(frame2, entry_kerrsup, *OPTIONS)
w.grid(row=1, column=2,pady= 5)

#FRAME 3
res_label = tk.Label(master=frame3, text="Reserve")
sen_label = tk.Label(master=frame3, text="Sensitivity")
tcon_label = tk.Label(master=frame3, text="Time constant")
fslope_label = tk.Label(master=frame3, text="Filter slope")

entry_res = tk.Entry(master=frame3, background="white")
entry_sen = tk.Entry(master=frame3, background="white")
entry_tcon = tk.Entry(master=frame3, background="white")
entry_fslope = tk.Entry(master=frame3, background="white")



res_label.grid(row=0, column=0)
sen_label.grid(row=0, column=2)
entry_res.grid(row=1, column=0,pady= 10)
entry_sen.grid(row=1, column=2,pady= 10)

tcon_label.grid(row=2, column=0,padx=5, pady= 10)
fslope_label.grid(row=2, column=2,padx=5,pady= 10)
entry_tcon.grid(row=3, column=0,padx=5,pady= 10)
entry_fslope.grid(row=3, column=2,padx=5,pady= 10)


#bbtn_run.grid(row=4, column=1,padx=5,pady= 10)

#FRAME 5
sample_label = tk.Label(master=frame5, text="Sample name")
fpath_label = tk.Label(master=frame5, text="File path")

entry_sample = tk.Entry(master=frame5, background="white")
entry_fpath = tk.Entry(master=frame5, background="white")

sample_label.grid(row=0, column=0)
fpath_label.grid(row=0, column=2)
entry_sample.grid(row=1, column=0,pady= 10)
entry_fpath.grid(row=1, column=2,pady= 10)

btn_run = tk.Button(
   master=frame5,
   text="RUN",
   command=main_function)

btn_run.grid(row=2, column=1,padx=5,pady= 10)


window.mainloop()