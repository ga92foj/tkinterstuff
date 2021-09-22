# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:32:49 2021

@author: moke
"""

"""
Spyder Editor
This is a temporary script file.
"""
import tkinter as tk
from tkinter import *
import random
import os
import time
import queue
from time import sleep
import threading
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import qcodes as qc
from qcodes.instrument_drivers.stanford_research.SR830 import SR830
from qcodes.utils.dataset import doNd
from qcodes import load_or_create_experiment
from qcodes.instrument.base import Instrument
from qcodes.utils.validators import Numbers
from qcodes.tests.instrument_mocks import DummyInstrument, DummyInstrumentWithMeasurement
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from matplotlib.figure import Figure

class GUI(tk.Tk):#how to structure this properly?

    def __init__(self):
        "make gui"
        super().__init__()
        self.main_container = tk.Frame(master=self, background="sienna")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.graph_container = tk.Frame(master=self, background="sienna")
        self.graph_container.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=0)
        frame1 = tk.Frame(master=self.main_container,bg='sienna', padx= 30, pady=30)
        frame2 = tk.Frame(master=self.main_container,bg='sienna', pady= 30)
        frame3 = tk.Frame(master=self.main_container,bg='sienna', padx= 30, pady=5)
        frame4 = tk.Frame(master=self.main_container,bg='sienna', padx= 30, pady=10)
        frame5 = tk.Frame(master=self.main_container,bg='sienna', padx= 30, pady=10)
        frame6 = tk.Frame(master=self.main_container,bg='sienna',padx=100)
        frame7 = tk.Frame(master=self.main_container,bg='sienna', padx= 30, pady=10)
        self.frame01 = tk.Frame(master=self.graph_container,bg='sienna', pady=50)



        frame1.grid(row=0, sticky="ew")
        frame2.grid(row=1, sticky="ew")
        frame3.grid(row=2, sticky="ew")
        frame5.grid(row=3, sticky="ew")
        frame5.grid(row=3, column=0, sticky="ew")
        frame6.grid(row=0, column=1, sticky="ew")
        frame7.grid(row=4, column=0, sticky="ew")
        self.frame01.grid(column=0)

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


        self.entry_nos = tk.Entry(master=frame1, background="white")
        self.entry_noa = tk.Entry(master=frame1, background="white")
        self.entry_minfield = tk.Entry(master=frame1, background="white")
        self.entry_maxfield = tk.Entry(master=frame1, background="white")


        nos_label.grid(row=3, column=0,padx=5,pady= 10)
        noa_label.grid(row=3, column=3,padx=5,pady= 10)
        self.entry_nos.grid(row=4, column=0,padx=5,pady= 10)
        self.entry_noa.grid(row=4, column=3,padx=5,pady= 10)

        minfield_label.grid(row=6, column=0,padx=5,pady= 10)
        maxfield_label.grid(row=6, column=3,padx=5,pady= 10)
        self.entry_minfield.grid(row=7, column=0,padx=5,pady= 10)
        self.entry_maxfield.grid(row=7, column=3,padx=5,pady= 10)


        #FRAME 2
        kerref_label = tk.Label(master=frame2, text='Kerr effect')
        kerrsup_label = tk.Label(master=frame2, text="Kerr signal")

        kerref_label.grid(row=0, column=0,padx=30, pady= 5)
        self.entry_kerref = tk.StringVar(frame1)
        self.entry_kerref.set(OPTIONS1[0]) # default value
        w = tk.OptionMenu(frame2, self.entry_kerref, *OPTIONS1)
        w.grid(row=1, column=0,padx= 30,pady= 5)

        kerrsup_label.grid(row=0, column=2,pady= 5,padx= 30)
        self.entry_kerrsup = tk.StringVar(frame1)
        self.entry_kerrsup.set(OPTIONS2[0]) # default value
        w = tk.OptionMenu(frame2, self.entry_kerrsup, *OPTIONS2)
        w.grid(row=1, column=2,pady= 5,padx= 30)

        #FRAME 3
        res_label = tk.Label(master=frame3, text="Reserve")
        sen_label = tk.Label(master=frame3, text="Sensitivity")
        tcon_label = tk.Label(master=frame3, text="Time constant")
        fslope_label = tk.Label(master=frame3, text="Filter slope")

        self.entry_res = tk.Entry(master=frame3, background="white")
        self.entry_sen = tk.Entry(master=frame3, background="white")
        self.entry_tcon = tk.Entry(master=frame3, background="white")
        self.entry_fslope = tk.Entry(master=frame3, background="white")



        res_label.grid(row=0, column=0)
        sen_label.grid(row=0, column=2)
        self.entry_res.grid(row=1, column=0,pady= 10)
        self.entry_sen.grid(row=1, column=2,pady= 10)

        tcon_label.grid(row=2, column=0,padx=5, pady= 10)
        fslope_label.grid(row=2, column=2,padx=5,pady= 10)
        self.entry_tcon.grid(row=3, column=0,padx=5,pady= 10)
        self.entry_fslope.grid(row=3, column=2,padx=5,pady= 10)


        #bbtn_run.grid(row=4, column=1,padx=5,pady= 10)
        #FRAME 5
        sample_label = tk.Label(master=frame5, text="Sample name")
        fpath_label = tk.Label(master=frame5, text="File path")
        loop_start_label= tk.Label(master=frame5, text="Start loop")
        loop_stop_label= tk.Label(master=frame5, text="End loop")

        self.entry_sample = tk.Entry(master=frame5, background="white")
        self.entry_fpath = tk.Entry(master=frame5, background="white")
        self.entry_loop_start=tk.Entry(master=frame5, background="white")
        self.entry_loop_stop= tk.Entry(master=frame5, background="white")

        sample_label.grid(row=0, column=0,padx=5,pady= 10)
        fpath_label.grid(row=0, column=2,padx=5,pady= 10)
        self.entry_sample.grid(row=1, column=0,padx=5,pady= 10)
        self.entry_fpath.grid(row=1, column=2,padx=5,pady= 10)
        loop_start_label.grid(row=2, column=0,padx=5,pady= 10)
        loop_stop_label.grid(row=2, column=2,padx=5,pady= 10)
        self.entry_loop_start.grid(row=3, column=0,padx=5,pady= 10)
        self.entry_loop_stop.grid(row=3, column=2,padx=5,pady= 10)
        
        self.title("MOKE CONTROL")
        self.current_mag_field=0
        btn_run = tk.Button(
           master=frame7,
           text="RUN",
           command=self.start1)

        btn_run.grid(row=2, column=0,padx=5,pady= 10)

        btn_run = tk.Button(
           master=frame7,
           text="CLOSE",
           command=close_function)

        btn_run.grid(row=2, column=2,padx=5,pady= 10)

        btn_run = tk.Button(
           master=frame7,
           text="STOP",
           command=self.force_stop)

        btn_run.grid(row=2, column=4,padx=5,pady= 10)
        
        btn_run = tk.Button(
           master=frame7,
           text="EXTRACT DATA",
           command=self.extract_data)

        btn_run.grid(row=4, column=2,padx=5,pady= 10)

        "read data"
        self.queue = queue.Queue()
        
        self.finish=0
        self.nos = 0
        self.noa = 0
        self.minfield = 0
        self.maxfield = 0
        self.kerref = 0
        self.kerrsup = 0

        self.sample_name = 0
        self.filepath = 0
        self.date_time = time.strftime("%Y%m%d-%H%M%S")
        self.date = time.strftime("%Y%m%d")
        self.timee = time.strftime("%H%M%S")


        self.loop_start = 0
        self.loop_end = 0

        self.time_con = 0
        self.res = 0
        self.sen = 0
        self.fslope = 0
        
        self.volt = 0
        
        self.mythread=None
        
        
        self.meas_values=['x','y','phase']
        
        self.listbox = tk.Listbox(master=frame5, width=20, height=5)
        self.listbox1 = tk.Listbox(master=frame5, width=20, height=5)

        self.e = threading.Event()
        
    def set_data(self):
        try:
            self.nos = int(self.entry_nos.get())
        except:
            print("Enter valid number of steps")
        try:
            self.noa = int(self.entry_noa.get())
        except:
            print("Enter valid number of averages")
        try:
            self.minfield = int(self.entry_minfield.get())
        except:
            print("Enter valid number target for magnetic field")
        try:
            self.maxfield = int(self.entry_maxfield.get())
        except:
            print("Enter valid number target for magnetic field")
        self.kerref = self.entry_kerref.get()
        self.kerrsup = self.entry_kerrsup.get()
    
        self.sample_name = self.entry_sample.get()
        self.filepath = self.entry_fpath.get()


 
        
        self.loop_start = self.entry_loop_start.get()
        self.loop_end = self.entry_loop_stop.get()
    
        self.time_con = self.entry_tcon.get()
        self.res = self.entry_res.get()
        self.sen = self.entry_sen.get()
        self.fslope = self.entry_fslope.get()
        
        self.volt = self.make_volt()
    
        self.meas_values=['x','y','phase']
        
        
        if not len(self.time_con) == 0:
            self.time_con=float(self.time_con)
            try:
                sr.time_constant(self.time_con)
            except:
                print("Enter valid time constant")
        else:
            self.time_con=0.03
        if not len(self.sen) == 0:
            try:
                sr.sensitivity(float(self.sen))
            except: 
                print("Enter valid time constant")
        if not len(self.fslope) == 0:
            sr.filter_slope(float(self.fslope))
        a=str(self.kerrsup)
        if a == "Rotation":
            sr.harmonic(2)
        if a == "Ellipticity":
            sr.harmonic(1)
        else:
            print('error')
            
        if len(self.filepath) == 0:
            self.filepath = r'C:\Users\moke\Desktop\PolLux\pythontests'
            
        self.filep= os.path.join(self.filepath, self.kerrsup+'_average_'+self.timee)   
        
    def force_stop(self):
        self.e.set()        
        
    def close_function(self):
        gui.destroy()
        
    def start1(self):
        self.set_data()
        volt=self.make_volt()
        #pass data to the threadedTask class  #(self, volt, noa, meas_values, time_con, filepath, sample_name, timee):
       # threadedTask(self.queue).sim_inheritance(volt, self.noa, self.meas_values, self.time_con, self.filepath, self.sample_name, self.timee)
        self.write_config()
        #sr.aux_out1(self.volt[0])
        #time.sleep(0.02)
        self.mythread=threadedTask(self.queue, volt, self.noa, self.meas_values, self.time_con, self.filepath, self.sample_name, self.timee, self.kerref, self.kerrsup, self.filep, self.e)
        self.mythread.start()
        self.after(100, self.process_queue)
    
    def process_queue(self):#https://stackoverflow.com/questions/16745507/tkinter-how-to-use-threads-to-preventing-main-event-loop-from-freezing
                            #https://stackoverflow.com/questions/15323574/how-to-connect-a-progress-bar-to-a-function/15323917#15323917

        try:                  
            msg = self.queue.get_nowait() #
            # Show result of the task if needed
            self.listbox.insert('end', msg)
            self.plot_stuff()
            print(msg)
        except queue.Empty:
            
            self.after(100, self.process_queue)
        
    def write_config(self):
        with open(os.path.join(self.filepath, self.sample_name+self.date_time+'configuration'), 'w') as fp:
            fp.write("Date\t"+self.date+"\tTime\t"+self.timee)
            fp.write("\nMeasured quantites:"+"\t"+ self.meas_values[0]+"\t" +self.meas_values[1]+"\t" +self.meas_values[2])
            linestowrite=["\nTime constant:", "Filter Slope:", "Sensitivity:", "Line filter:", "Reserve:", "Number of steps:", "Number of averages:"]
            linetowrit1 = ["\n" + str(sr.time_constant()), str(sr.filter_slope), str(sr.sensitivity()), "", str(sr.reserve()), str(self.nos), str(self.noa)]
            for i,j in zip(linestowrite, linetowrit1):
                fp.write(i+"\t")
                fp.write(j+"\t")
                
    def track_mag_field(self):
        cur_mag_field=sr.snap('x','y')
        print(cur_mag_field)
    def get_mag_array_l2r(self, nos, start1, stop1, min_mag, max_mag):
        mag_array0=np.linspace(min_mag,start1,nos//3)
        max_array1=np.linspace(start1,stop1,nos//3)
        max_array2=np.linspace(stop1,max_mag,nos//3)
        return np.concatenate((mag_array0,max_array1,max_array2),axis=None)
    
    def get_mag_array_r2l(self, nos, start1, stop1, min_mag, max_mag):
        mag_array0=np.linspace(max_mag,stop1,nos//3)
        max_array1=np.linspace(stop1,start1,nos//3)
        max_array2=np.linspace(start1,min_mag,nos//3)
        return np.concatenate((mag_array0,max_array1,max_array2),axis=None)
    def make_volt(self):
        if (len(str(self.loop_start)) != 0 and len(str(self.loop_end)) != 0):
            print("custom volt")
            self.loop_start=float(self.loop_start)
            self.loop_end=float(self.loop_end)
            mag_f=self.get_mag_array_l2r(self.nos, self.loop_start,self.loop_end, self.minfield, self.maxfield)
            mag_b=self.get_mag_array_r2l(self.nos, self.loop_start,self.loop_end, self.minfield, self.maxfield)
            self.volt=np.concatenate((mag_f,mag_b),axis=None)/1600
        else:
            minvolt=self.minfield/1600
            maxvolt=self.maxfield/1600
            volt1=np.linspace(minvolt,maxvolt,self.nos)
            volt2=np.linspace(maxvolt,minvolt,self.nos)
            self.volt=np.concatenate((volt1,volt2),axis=None)
        return self.volt
    
    def plot_stuff(self):
        mat=np.array(np.loadtxt(self.filep))
        fig, ax=plt.subplots(figsize=(12, 10))
        fig.tight_layout(pad=15)
        ax.scatter(mat[:,0]*1600,mat[:,1])
        ax.plot(mat[:,0]*1600,mat[:,1])
        ax.set_title('X Signal strength',fontsize= 30)
        ax.set_xlabel('Magnetic field in mT',fontsize = 20)
        ax.set_ylabel('X', fontsize = 20, labelpad=15)
        plt.yticks(fontsize=13)
        plt.xticks(fontsize=13)
        graph_1 = FigureCanvasTkAgg(fig, master=self.frame01)
        graph_1.get_tk_widget().pack()
        graph_1.draw()
        
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(graph_1,
                               self.frame01)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        graph_1.get_tk_widget().pack()
    def extract_data(self):
        filep=r'C:\Users\moke\Desktop\PolLux\tests\pythontests\_goodtests\5timecon6dblownoise_nicedriftcorrection'
        print(filep)
        from class_upgrade import myloop
        a = myloop(filep)
        a.correct_drift(3)
        print('Calculated coercivity value %2.4f' %a.get_coercivity(2))
        print('Calculated saturation value %2.12f' %a.myhisto(0)[0])
        print('Calculated saturation value %2.12f' %a.myhisto(0)[1])
        print('Signal to noise ratio %2.2f' %a.get_snr()[0])
        print('Signal to noise ratio in dB %2.2f' %a.get_snr()[1])
        
        
        
class threadedTask(threading.Thread):#Is it better to inherit from 2 classes?
    
    def __init__(self, queue,volt, noa, meas_values, time_con, filepath, sample_name, timee, kerref, kerrsup, filep, e):
        super(threadedTask,self).__init__()
        self.queue = queue
        self.e=e
        self.volt=volt
        self.noa=noa
        self.meas_values=meas_values
        self.time_con=time_con
        self.filepath=filepath
        self.sample_name=sample_name
        self.timee=time
        self.kerreff=kerref
        self.kerrsup=kerrsup
        self.filep=filep
    def run(self):
        
        #self.reading_values()
        # Simulate long running process
        self.reading_values()
        

    def reading_values(self):
        global stop
        start_time=time.perf_counter()
        #a = Main(window)
        average_X = np.zeros([self.volt.size, self.noa])
        average_Y = np.zeros([self.volt.size, self.noa])
        average_phase = np.zeros([self.volt.size, self.noa])
        mes1=self.meas_values[0]
        mes2=self.meas_values[1]
        mes3=self.meas_values[2]
        sr.reserve('low noise')
        sr.sensitivity(0.0005)
        sr.notch_filter('line in')
        sr.filter_slope(6)
        for j in range(self.noa):
            results=np.zeros([self.volt.size,4])
            results[:,0]=self.volt
            sr.auto_phase()
            time.sleep(0.02)
            for i in range(self.volt.size):
                cur_volt=self.volt[i]
                sr.aux_out1.set(cur_volt)
                time.sleep(6*self.time_con)
                _=np.array(sr.snap('x','y','r'))
                results[i,[0]]=sr.aux_out1.get()
                results[i,[1,2,3]]=_
                if self.e.isSet():
                    print("broken")
                    sr.aux_out1.set(0)
                    time.sleep(self.time_con)
                    break
                print("current mag field: ")
                print(sr.aux_out1.get()*1600)
            with open((os.path.join(self.filepath,self.kerrsup+'_loop_'+str(j))), 'w+') as fp:
                np.savetxt(fp,results)
                fp.close()
        time.sleep(self.time_con)
        sr.aux_out1.set(0)
        average_X[:,j]=results[:,1]
        average_Y[:,j]=results[:,2]
        average_phase[:,j]=results[:,3]
        
        end_time=time.perf_counter()
        timearray=np.linspace(start_time, end_time, self.volt.size)-start_time
    
        average_results=np.zeros([self.volt.size,4])
        average_results[:,0]=self.volt
        average_results[:,1]=np.mean(average_X,axis=1)
        average_results[:,2]=np.mean(average_Y,axis=1)
        average_results[:,3]=np.mean(average_phase,axis=1)
        mat = np.matrix(average_results)    
        self.queue.put("Task finished")
        with open(self.filep, 'w+') as fp:
            np.savetxt(fp, mat)
            fp.close()
        #os.path.join(self.filepath, (self.filepath,'average'+self.timee))
    def set_data2(self, volt, noa, nos, meas_values, time_con, filepath, sample_name, timee):
        self.volt=volt
        self.noa=noa
        self.nos=nos
        self.meas_values=meas_values
        self.time_con=time_con
        self.filepath=filepath
        self.sample_name=sample_name
        self.timee=timee

#plt.ylabel('Y')
#plt.xlabel("magnetic field")
#ax[1].plot(mat[:,0],mat[:,2])
# f = plt.Figure(figsize=(5,4), dpi=100)
# a = f.add_subplot(111)
# a.plot(mat[:,0],mat[:,1])
    #graph_1 = FigureCanvasTkAgg(fig, master=frame01)
    #graph_1.get_tk_widget().grid(row = 0, column = 0)
    #graph_1.draw()

"""fig2, ax2=plt.subplots(2,1,sharey=True)
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
graph_2.draw()"""

#fig2, ax2=plt.subplots(1,1,tight_layout=True)
#plt.ylabel('X')
#plt.xlabel("time")
#plt.plot(timearray,mat[:,1])
#graph_2 = FigureCanvasTkAgg(fig1, master=frame02)
#graph_2.get_tk_widget().grid(row = 2, column = 0)
#graph_2.draw()"""
        
        
        
        
        

def close_function():
    gui.destroy()
    

"""def start1():
    a = Main(window)
    a.set_parameters()
    sr.aux_out1(a.volt[0])
    time.sleep(0.02)
    a.write_config()
    #meas_quan_label = tk.Label(master=frame1, text='Currently measuring'+"\n"+a.meas_values[0]+\
                               #"\n"+a.meas_values[1]+"\n"+a.meas_values[2])
    
    def reading_values():
        start_time=time.perf_counter()
        #a = Main(window)
        volt=a.volt
        noa=a.noa
        average_X = np.zeros([volt.size, noa])
        average_Y = np.zeros([volt.size, noa])
        average_phase = np.zeros([volt.size, noa])
        mes1=a.meas_values[0]
        mes2=a.meas_values[1]
        mes3=a.meas_values[2]
        for j in range(noa):
            results=np.zeros([volt.size,4])
            results[:,0]=volt
            sr.auto_phase()
            time.sleep(0.02)
            if not force_stop:
                for i in range(volt.size):
                    cur_volt=volt[i]
                    sr.aux_out1.set(cur_volt)
                    time.sleep(3*a.time_con)
                    _=np.array(sr.snap(mes1,mes2,mes3))
                    results[i,[0]]=sr.aux_out1.get()
                    results[i,[1,2,3]]=_
                    if force_stop:
                        print("broken")
                        break
                    print("current mag field: ")
                    print(sr.aux_out1.get()*1600)           
                with open((os.path.join(a.filepath, a.sample_name + a.timee+str(j))), 'w+') as fp:
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
        mat = np.matrix(average_results)
        

        return

        
    t1 = threading.Thread(target=reading_values)
    t1.start()"""
    
def plot_stuff(graph):
    from class_upgrade import myloop    
    #frame01 = tk.Frame(master=window1,bg='white', height=500, padx= 30, pady= 30)
    #frame02 = tk.Frame(master=window1,bg='white', height=500, padx= 30, pady=5)
    #frame03 = tk.Frame(master=window1,bg='white', height=500, padx= 30, pady=10)
    
    #frame01.grid(row=0, sticky="ew")
    #frame02.grid(row=1, sticky="ew")
    #frame03.grid(row=2, sticky="ew")
    
    loop=myloop(os.path.join(self.filepath, self.sample_name + '_average'+'_'+self.kerref+'_'+self.kerrsup))
    filep=os.path.join(self.filepath, self.sample_name + '_average'+'_'+self.kerref+'_'+self.kerrsup)
    fig, ax=plt.subplots()
    plt.ylabel('X')
    plt.xlabel("magnetic field")
    ax.plot(mat[:,2],mat[:,1])
    #plt.ylabel('Y')
    #plt.xlabel("magnetic field")
    #ax[1].plot(mat[:,0],mat[:,2])
   # f = plt.Figure(figsize=(5,4), dpi=100)
   # a = f.add_subplot(111)
   # a.plot(mat[:,0],mat[:,1])
    graph_1 = FigureCanvasTkAgg(fig, master=frame01)
    graph_1.get_tk_widget().grid(row = 0, column = 0)
    graph_1.draw()
    
   # fig2, ax2=plt.subplots(2,1,sharey=True)
    #plt.ylabel('R')
   # plt.xlabel("time")
    #ax2[0].plot(timearray,mat[:,3])
    #plt.ylabel('X')
    #plt.xlabel("time")
    #ax2[1].plot(timearray,mat[:,1])
    #ax2[0].set(title='Temporal evolution', xlabel='Time', ylabel='R')
    #ax2[1].set(title='Temporal evolution', xlabel='Time', ylabel='X')
    
    #graph_2 = FigureCanvasTkAgg(fig2, master=frame02)
    #graph_2.get_tk_widget().grid(row = 1, column = 0)
    #graph_2.draw()

    #fig2, ax2=plt.subplots(1,1,tight_layout=True)
    #plt.ylabel('X')
    #plt.xlabel("time")
    #plt.plot(timearray,mat[:,1])
    #graph_2 = FigureCanvasTkAgg(fig1, master=frame02)
    #graph_2.get_tk_widget().grid(row = 2, column = 0)
    #graph_2.draw()

if __name__ == "__main__":
    #initialize
    #window1 = tk.Tk()
    r=random.randint(1, 1000)
    sr = SR830('lockin'+str(r), 'GPIB0::5::INSTR')
    gui = GUI()
    gui.mainloop()


