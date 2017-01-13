# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 12:02:51 2016

@author: Keith
"""

# basic imports
import os, sys, glob, pdb
import urllib
import numpy as np
from numpy import array
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt

def explore(station_id):
    
    NO_DATA = -999

    df = pd.read_csv('E:\\temps\\clean\\merge\\station_' + station_id + '.csv')
            
    for field in ['tmax', 'tmin']:
        t = array(df[field]).astype('float')
        t[t==NO_DATA] = np.nan
        t_arr  = np.reshape(t, (100,365))
        t_mean = np.nanmean(t_arr, axis=0)
        t_std  = np.nanstd(t_arr, axis=0)
            
        #plt.plot(array([t_std + t_mean, t_mean, t_mean - t_std]).transpose())
        
    t_min = array(df['tmin']).astype('float')
    t_max = array(df['tmax']).astype('float')
    
    t_arr = np.reshape(t_min, (100,365))
        
    MIN = t_min[t_min!=NO_DATA].min()
    MAX = t_max.max()
        
    binWidth = 5
    bins = np.arange(MIN, MAX + binWidth, binWidth)
        
    t_min_arr = np.reshape(t_min, (100,365))
    t_max_arr = np.reshape(t_max, (100,365))        
        
    h_arr = np.zeros((len(bins)-1, 365, 3))
   
    dayWindow = 2    
    for doy in range(2,364):
            
        t_doy = t_min_arr[:, doy - dayWindow : doy + dayWindow + 1].ravel()
        h, e = np.histogram(t_doy[t_doy!=NO_DATA], bins)
        h_arr[:,doy,0] = h #255*h/h.max()
        
        t_doy = t_max_arr[:, doy - dayWindow : doy + dayWindow + 1].ravel()
        h, e = np.histogram(t_doy[t_doy!=NO_DATA], bins)
        h_arr[:,doy,1] = h #255*h/h.max()
    
    h_arr_disp = h_arr
    h_arr_disp[:,:,0] = 255*h_arr[:,:,0] / h_arr[:,:,0].ravel().max()
    h_arr_disp[:,:,1] = 255*h_arr[:,:,1] / h_arr[:,:,1].ravel().max()

    plt.figure()
    plt.imshow(h_arr.astype('uint8'), interpolation='nearest', origin='low', aspect='auto')
    
    return h_arr, bins
    
    
def replaceNoDataFlag(csvDir):
    
    csvs = glob.glob(csvDir + '*.csv')
    
    for csv in csvs:
        
        if (csv.find('mean') > 0):
            continue   
        
        print(csv)
        
        d = pd.read_csv(csv)
        
        mk = np.array(d.tmin==-999) + np.array(d.tmax==-999)
        
        d.tmin.iloc[mk] = float(np.nan)
        d.tmax.iloc[mk] = float(np.nan)
        
        d.to_csv(csv, index=False)
    
def calcMeanOverTime(csvDir):
    
    # calculate the mean tmin and tmax for each day of the year
    # saves loading a large CSV in the browser
    
    NO_DATA = -999

    csvs = glob.glob(csvDir + '*.csv')
    
    for csv in csvs:

        
        dest = csvDir + csv.split('\\')[-1][:-4] + '_mean.csv'
        
        print(dest)
        
        data = pd.read_csv(csv)
        
        data.tmin
        
        meanByDay = pd.DataFrame({'doy': range(1,366), 'tmin': np.zeros((365,)), 'tmax': np.zeros((365,))})
        
        for ind, row in meanByDay.iterrows():
            
            # note: assignment using meanByDay.iloc[ind].tmin = __ is *very* slow
                        
            t_ = data.loc[data.doy==row.doy].tmin
            row.tmin = round(t_[t_!=NO_DATA].mean(), 2)
            
            t_ = data.loc[data.doy==row.doy].tmax
            row.tmax = round(t_[t_!=NO_DATA].mean(), 2)
            
            meanByDay.iloc[ind] = row
            
        meanByDay.to_csv(dest, index=False)
    
    
def addMeansToMetadata(metadata):
    
    for ind, row in metadata.iterrows():
        
        id = list(str(row.id))
        
        id[0] = id[0].replace('0', '')
        
        print(''.join(id))
        data = pd.read_csv('stations\\station_' + ''.join(id) + '_mean.csv')
        
        metadata.mhigh[ind] = data.tmax.mean()
        metadata.mlow[ind] = data.tmin.mean()
        
    return metadata
        
    
def simplify():
    
    # simplify the data by eliminating redundant date columns
    # retain only number of years since 1911, the day of the year, and the temp
    
    localSourceDir = 'E:\\temps\\raw\\'
    localDestDir = 'E:\\temps\\clean\\'
    
    subDirs = ['tmax\\', 'tmin\\']
    
    for subDir in subDirs:
        
        txts = glob.glob(localSourceDir + subDir + '*.txt')
        
        for txt in txts:
            
            print(txt)
            
            df = pd.read_csv(txt, sep='\s+', header=None)
            
            station_id = df[0][0]
            
            doy  = df[1]            
            year = df[2]        
            temp = df[5]
            
            # years since 1911
            year = year - 1911
            
            df_new = pd.DataFrame({'year': year, 'doy': doy, subDir[:-1]: temp})
            
            df_new.to_csv(localDestDir + subDir + 'station_' + str(station_id) + '.csv', index=False)            
            
            
def mergetmintmax():
    
    # merge tmax and tmin files into one csv with tmax and tmin columns
    
    localDir = 'E:\\temps\\clean\\'
    
    csvs_max = glob.glob(localDir + 'tmax\\*.csv')
    
    for csv_max in csvs_max:
        
        print(csv_max)
        
        fname = csv_max.split('\\')[-1]
        
        csv_min = localDir + 'tmin\\' + fname
    
        dx = pd.read_csv(csv_max)
        dn = pd.read_csv(csv_min)
        
        dn['tmax'] = dx.tmax
        
        dn.to_csv('E:\\temps\\clean\\merge\\' + fname, index=False)
        
    

def download():
    
    remoteURL = 'http://cdiac.ornl.gov/ftp/us_recordtemps/sta424/tmin_serial/'
    localDir  = 'E:\\temps\\data\\'
                
    # station metadata
    stations = pd.read_csv(os.getcwd() + '\\USHCN-network-metadata.clean.txt', sep='\s+')

    for ind, station in stations.iterrows():

        # format of the txt file names - state + last four digits of station ID        
        fname = station.state + '_' + str(station.id)[-4:] + 'tmin.txt'        

        print(fname)
        
        try:
            urllib.urlretrieve(remoteURL + fname, localDir + fname)
        except Exception as err:
            print(type(err))