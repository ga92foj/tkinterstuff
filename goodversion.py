# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import tkinter as tk
from tkinter import *
import random
import os
import time
from time import sleep
import threading
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import qcodes as qc
import numpy as np
from qcodes.instrument_drivers.stanford_research.SR830 import SR830
from qcodes.utils.dataset import doNd
from qcodes import load_or_create_experiment
from qcodes.instrument.base import Instrument
from qcodes.utils.validators import Numbers
from qcodes.tests.instrument_mocks import DummyInstrument, DummyInstrumentWithMeasurement
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure




def close_function():
    window.destroy()
    
def get_mag_array_l2r(nos, start1, stop1, min_mag, max_mag):
    mag_array0=np.linspace(min_mag,start1,nos//3)
    max_array1=np.linspace(start1,stop1,nos//3)
    max_array2=np.linspace(stop1,max_mag,nos//3)
    return np.concatenate((mag_array0,max_array1,max_array2),axis=None)

def get_mag_array_r2l(nos, start1, stop1, min_mag, max_mag):
    mag_array0=np.linspace(max_mag,stop1,nos//3)
    max_array1=np.linspace(stop1,start1,nos//3)
    max_array2=np.linspace(start1,min_mag,nos//3)
    return np.concatenate((mag_array0,max_array1,max_array2),axis=None)

def set_force_stop():
    global force_stop
    force_stop=True
    
def set_voltage(voltage, tim_c):
    time_conn=int(tim_c*1000)
    sr.aux_out1(voltage)
    
def main_function():
    force_stop=False
    "read data"
    nos = int(entry_nos.get())
    noa = int(entry_noa.get())
    minfield = int(entry_minfield.get())
    maxfield = int(entry_maxfield.get())
    kerref = entry_kerref.get()
    kerrsup = entry_kerrsup.get()
    
    
    sample_name=entry_sample.get()
    filepath=entry_fpath.get()
    date_time=time.strftime("%Y%m%d-%H%M%S")
    date=time.strftime("%Y%m%d")
    timee=time.strftime("%H%M%S")
    
    if len(filepath)==0:
        filepath=r'C:\Users\moke\Desktop\PolLux\tests\pythontests'
        
    loop_start=entry_loop_start.get()
    loop_end=entry_loop_stop.get()
    
    
    time_con=entry_tcon.get()
    res=entry_res.get()
    sen=entry_sen.get()
    fslope=entry_fslope.get()
    
    
    "set it to sr830"
    if not len(time_con) == 0:
        time_con=float(time_con)
        sr.time_constant(time_con)
    else:
        time_con=0.03
    if not len(sen) == 0:
       sr.sensitivity(float(sen))
    if not len(fslope) == 0:
        sr.filter_slope(float(fslope))
        
    if (len(loop_start) != 0 and len(loop_end) != 0):
        loop_start=float(loop_start)
        loop_end=float(loop_end)
        mag_f=get_mag_array_l2r(nos, loop_start,loop_end, minfield, maxfield)
        mag_b=get_mag_array_r2l(nos, loop_start,loop_end, minfield, maxfield)
        volt=np.concatenate((mag_f,mag_b),axis=None)/1600
    else:
        minvolt=minfield/1600
        maxvolt=maxfield/1600
        volt1=np.linspace(minvolt,maxvolt,nos)
        volt2=np.linspace(maxvolt,minvolt,nos)
        volt=np.concatenate((volt1,volt2),axis=None)
    #sr.sensitivity(sen)
    #sr.filter_slope(fslope)
    #sr.reserve(res)
    "set harmonic"
    print(kerrsup)
    a=kerrsup
    print(a)
    if kerrsup == "Rotation":
        sr.harmonic(2)
    elif  str(a) == "Ellipticity":
        sr.harmonic(1)
    else:
        print('error')
    "set it to minimal voltage"
    set_voltage(minvolt, time_con)
    while abs(sr.aux_out1()-volt[0])>0.001:
        time.sleep(0.02)
    print("first step")
    print(sr.aux_out1()*1600)
    "array of all the voltages"

    average_X=np.zeros([volt.size,noa])
    average_Y=np.zeros([volt.size,noa])
    average_phase=np.zeros([volt.size,noa])
    
    
    start_time=time.perf_counter()

    
    for j in range(noa):
        if force_stop:
            break
        results=np.zeros([volt.size,4])
        results[:,0]=volt
        sr.auto_phase()
        window.after(int(20))
        if not force_stop:
            for i in range(volt.size):
                cur_volt=volt[i]
                window.after(int(3*time_con*1000),set_voltage(cur_volt*1600,time_con))
                _=np.array(sr.snap('x','aux1','r'))
                results[i,[0]]=sr.aux_out1.get()
                results[i,[1,2,3]]=_
                if force_stop:
                    return
                print("current mag field: ")
                print(sr.aux_out1.get()*1600)           
            with open((os.path.join(filepath, sample_name + timee+str(j))), 'w+') as fp:
                np.savetxt(fp,results)
                fp.close()
        average_X[:,j]=results[:,1]
        average_Y[:,j]=results[:,2]
        average_phase[:,j]=results[:,3]
            
    end_time=time.perf_counter()
    timearray=np.linspace(start_time, end_time, volt.size)-start_time

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
    mat = np.matrix(average_results)
    with open(os.path.join(filepath, sample_name + '_average'+'_'+kerref+'_'+kerrsup), 'w+') as fp:
            np.savetxt(fp, mat)
            fp.close()
    """first_half=np.split(average_results[:,0])[0]#finding value closest to 0
    second_half=np.split(average_results[:,0])[1]#finding value closest to 0
    index1=np.argmin(abs(first_half))
    index2=np.argmin(abs(second_half))
    first_half_X=np.split(average_results[:,1])[0]
    second_half_X=np.split(average_results[:,1])[1]
    zero_first_half=first_half_X[index1]#magnetic field at 0
    zero_second_half=second_half_X[index2]#magnetic field at 0

    signal_str= zero_first_half-zero_second_half
    average_X1=average_results[:,1]-first_half_X+signal_str/2"""
    
    
    from class_upgrade import myloop    
    frame01 = tk.Frame(master=window1,bg='white', height=500, padx= 30, pady= 30)
    frame02 = tk.Frame(master=window1,bg='white', height=500, padx= 30, pady=5)
    frame03 = tk.Frame(master=window1,bg='white', height=500, padx= 30, pady=10)
    
    frame01.grid(row=0, sticky="ew")
    frame02.grid(row=1, sticky="ew")
    frame03.grid(row=2, sticky="ew")
    
    loop=myloop(os.path.join(filepath, sample_name + '_average'+'_'+kerref+'_'+kerrsup))
    filep=os.path.join(filepath, sample_name + '_average'+'_'+kerref+'_'+kerrsup)
    fig, ax=plt.subplots()
    plt.ylabel('X')
    plt.xlabel("magnetic field")
    ax.plot(mat[:,2],mat[:,1])
    ax.set(title='X', xlabel='Magnetic field', ylabel = 'X')
    #plt.ylabel('Y')
    #plt.xlabel("magnetic field")
    #ax[1].plot(mat[:,0],mat[:,2])
   # f = plt.Figure(figsize=(5,4), dpi=100)
   # a = f.add_subplot(111)
   # a.plot(mat[:,0],mat[:,1])
    graph_1 = FigureCanvasTkAgg(fig, master=frame01)
    graph_1.get_tk_widget().grid(row = 0, column = 0)
    graph_1.draw()
    
    fig2, ax2=plt.subplots(2,1,sharey=True)
    plt.ylabel('R')
    plt.xlabel("time")
    ax2[0].plot(timearray,mat[:,3])
    plt.ylabel('X')
    plt.xlabel("time")
    ax2[1].plot(timearray,mat[:,1])
    ax2[0].set(title='Temporal evolution', xlabel='Time', ylabel='R')
    ax2[1].set(title='Temporal evolution', xlabel='Time', ylabel='X')
    
    graph_2 = FigureCanvasTkAgg(fig2, master=frame02)
    graph_2.get_tk_widget().grid(row = 1, column = 0)
    graph_2.draw()

    #fig2, ax2=plt.subplots(1,1,tight_layout=True)
    #plt.ylabel('X')
    #plt.xlabel("time")
    #plt.plot(timearray,mat[:,1])
    #graph_2 = FigureCanvasTkAgg(fig1, master=frame02)
    #graph_2.get_tk_widget().grid(row = 2, column = 0)
    #graph_2.draw()
    
window = tk.Tk()
window.title("MOKE CONTROL")
window1 = tk.Tk()
a=random.randint(1, 1000)
sr = SR830('lockin'+str(a), 'GPIB0::5::INSTR')


frame1 = tk.Frame(master=window,bg='black', width=1000, height=1500, padx= 30, pady=30)
frame2 = tk.Frame(master=window,bg='black', height=500, padx= 30, pady= 30)
frame3 = tk.Frame(master=window,bg='black', height=500, padx= 30, pady=5)
frame4 = tk.Frame(master=window,bg='black', height=1000, padx= 30, pady=10)
frame5 = tk.Frame(master=window,bg='black', height=500, padx= 30, pady=10)
frame6 = tk.Frame(master=window,bg='black',padx=100)
frame7 = tk.Frame(master=window,bg='black', padx= 30, pady=10)



frame1.grid(row=0, sticky="ew")
frame2.grid(row=1, sticky="ew")
frame3.grid(row=2, sticky="ew")
frame5.grid(row=3, sticky="ew")
frame5.grid(row=3, column=0, sticky="ew")
frame6.grid(row=0, column=1, sticky="ew")
frame7.grid(row=4, column=0, sticky="ew")



OPTIONS1 = [
"Longitudinal",
"Polar",
"Transverse"
]
OPTIONS2 = [
"Rotation",
"Ellipticity",
]
#FRAME 1

VISA_label = tk.Label(master=frame1, text='VISA resource name')
nos_label = tk.Label(master=frame1, text="Number of steps")
noa_label = tk.Label(master=frame1, text='Number of averages')
minfield_label = tk.Label(master=frame1, text='Min magn field')
maxfield_label = tk.Label(master=frame1, text='Max magn field')

#VISA_label.grid(row=0, column=1,pady= 5)
#entry_VISA = tk.StringVar(frame1)
#entry_VISA.set(OPTIONS1[0]) # default value
#w = tk.OptionMenu(frame1, entry_VISA, *OPTIONS1)
#w.grid(row=1, column=1,pady= 5)


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
entry_kerref.set(OPTIONS1[0]) # default value
w = tk.OptionMenu(frame2, entry_kerref, *OPTIONS1)
w.grid(row=1, column=0,pady= 5)

kerrsup_label.grid(row=0, column=2,pady= 5,padx= 20)
entry_kerrsup = tk.StringVar(frame1)
entry_kerrsup.set(OPTIONS2[0]) # default value
w = tk.OptionMenu(frame2, entry_kerrsup, *OPTIONS2)
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
loop_start_label= tk.Label(master=frame5, text="Start loop")
loop_stop_label= tk.Label(master=frame5, text="End loop")

entry_sample = tk.Entry(master=frame5, background="white")
entry_fpath = tk.Entry(master=frame5, background="white")
entry_loop_start=tk.Entry(master=frame5, background="white")
entry_loop_stop= tk.Entry(master=frame5, background="white")

sample_label.grid(row=0, column=0)
fpath_label.grid(row=0, column=2)
entry_sample.grid(row=1, column=0,pady= 10)
entry_fpath.grid(row=1, column=2,pady= 10)
loop_start_label.grid(row=2, column=0)
loop_stop_label.grid(row=2, column=2)
entry_loop_start.grid(row=3, column=0)
entry_loop_stop.grid(row=3, column=2)




btn_run = tk.Button(
   master=frame7,
   text="RUN",
   command=main_function)

btn_run.grid(row=2, column=0,padx=5,pady= 10)

btn_run = tk.Button(
   master=frame7,
   text="CLOSE",
   command=close_function)

btn_run.grid(row=2, column=2,padx=5,pady= 10)

window.mainloop()