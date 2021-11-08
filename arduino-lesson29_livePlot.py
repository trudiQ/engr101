#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Trudi Qi (dqi@chapman.edu)
# Created Date: Fri Nov 5 2021 2:30 PM
# version ='1.0'
# ---------------------------------------------------------------------------
#%%
# Import libraries
import time
import serial
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# animation function
#   - ser is the serial port of arduino
#   - df is pandas dataframe
def animation(i, ser, df, acx_list, acy_list, acz_list, tmp_list, gyx_list, gyy_list, gyz_list): 
    # read data from serial port
    serString = ser.readline()
    
    # convert the data to string
    serString = str(serString, encoding = 'utf-8') 
    
    # split string to an array of data elements
    dataArray = serString.split(' | ')
    
    # save the array of data elements to dataframe df
    index = len(df.index)
    #print(dataArray)
    
    # feed the data to dataframe
    df.loc[index] = [
    dataArray[0].split(' = ')[1],
    dataArray[1].split(' = ')[1],
    dataArray[2].split(' = ')[1],
    dataArray[3].split(' = ')[1],
    dataArray[4].split(' = ')[1],
    dataArray[5].split(' = ')[1],
    dataArray[6].split(' = ')[1].replace("\r\n", "")]
    
    # save dataframe df to CSV
    df.loc[index:].to_csv('test.csv', index=False, mode = 'a', header=False)
    
    # add the data to the lists for plotting
    acx_list.append(float(df.loc[index, 'AcX']))
    acy_list.append(float(df.loc[index, 'AcY']))
    acz_list.append(float(df.loc[index, 'AcZ']))
    tmp_list.append(float(df.loc[index, 'Tmp']))
    gyx_list.append(float(df.loc[index, 'GyX']))
    gyy_list.append(float(df.loc[index, 'GyY']))
    gyz_list.append(float(df.loc[index, 'GyZ']))
    
    # limit the data to 100 values
    acx_list = acx_list[-100:]
    acy_list = acy_list[-100:]
    acz_list = acz_list[-100:]
    tmp_list = tmp_list[-100:]
    gyx_list = gyx_list[-100:]
    gyy_list = gyy_list[-100:]
    gyz_list = gyz_list[-100:]
    #print('acx: ' + str(acx_list))
    #print('acy: ' + str(acy_list))
    #print('acz: ' + str(acz_list))
    #print('tmp: ' + str(tmp_list))
    #print('gyx: ' + str(gyx_list))
    #print('gyy: ' + str(gyy_list))
    #print('gyz: ' + str(gyz_list))
    
    # clear the last frame and draw the next frame
    ax0.clear()
    ax0.plot(acx_list, color='C0')
    ax1.clear()
    ax1.plot(acy_list, color='C1')
    ax2.clear()
    ax2.plot(acz_list, color='C2')
    ax3.clear()
    ax3.plot(tmp_list, color='C3')
    ax4.clear()
    ax4.plot(gyx_list, color='C4')
    ax5.clear()
    ax5.plot(gyy_list, color='C5')
    ax6.clear()
    ax6.plot(gyz_list, color='C6')
    
    # format plot
    ax0.set_title("MPU 6050 Reading Live Plot")
    ax0.set_ylabel("AcX")
    ax1.set_ylabel("AcY")
    ax2.set_ylabel("AcZ")
    ax3.set_ylabel("Tmp")
    ax4.set_ylabel("GyX")
    ax5.set_ylabel("GyY")
    ax6.set_ylabel("GyZ")
    

# Create empty list to store data
acx_list = []
acy_list = []
acz_list = []
tmp_list = []
gyx_list = [] 
gyy_list = []
gyz_list = []

# Create a new figure with 7 rows of sub-plots (axes)
fig, (ax0, ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(7, 1)

# Create a new CSV file linked to a dataFrame 
df = pd.DataFrame(columns = ["AcX", "AcY", "AcZ", "Tmp", "GyX", "GyY", "GyZ"]) # header of the CSV
df.to_csv('test.csv', index=False) # give the file name

# Find the arduino serial port
ser = serial.Serial('COM6', 9600)
#time.sleep(2)
print(ser.name)

# Makes an plotting animation by repeatedly calling 'animation' function
#   - Reading data from 'ser', plotting live data, saving data to CSV
ani = FuncAnimation(fig, animation, frames=100, fargs=(ser, df, acx_list, acy_list, acz_list, 
                                                        tmp_list, gyx_list, gyy_list, gyz_list), interval=100)

# Adjust figure layout and display the figure 
plt.subplots_adjust(left=0.15)
plt.show()

# after the window is closed, close the serial line
ser.close()
print("Serial line closed")

'''
# animation function
#   - ser is the serial port of arduino
#   - df is pandas dataframe
def animation(i, data_list, ser, df): 
    # read data from serial port
    serString = ser.readline()
    
    # convert the data to string
    serString = str(serString, encoding = 'utf-8') 
    
    # split string to an array of data elements
    dataArray = serString.split(' | ')
    
    # save the array of data elements to dataframe df
    index = len(df.index)
    #print(dataArray)
    
    # feed the data to dataframe
    df.loc[index] = [
    dataArray[0].split(' = ')[1],
    dataArray[1].split(' = ')[1],
    dataArray[2].split(' = ')[1],
    dataArray[3].split(' = ')[1],
    dataArray[4].split(' = ')[1],
    dataArray[5].split(' = ')[1],
    dataArray[6].split(' = ')[1].replace("\r\n", "")]
    
    # save dataframe df to CSV
    df.loc[index:].to_csv('test.csv', index=False, mode = 'a', header=False)
    
    # add the data to the list for plotting
    data_list.append(float(df.loc[index].GyX))
    
    # limit the data to 100 values
    data_list = data_list[-100:]
    #print(data_list)
    
    # clear the last frame and draw the next frame
    ax.clear()
    ax.plot(data_list)
    
    # format plot
    #ax.set_ylim([-15000, 15000])
    #ax.autoscale_view()
    ax.set_title("MPU 6050 Reading Live Plot")
    ax.set_ylabel("GyX Reading")
    

# Create empty list to store data
data_list = []
fig, ax = plt.subplots()

# Create a new CSV file linked to a dataFrame 
df = pd.DataFrame(columns = ["AcX", "AcY", "AcZ", "Tmp", "GyX", "GyY", "GyZ"]) # header of the CSV
df.to_csv('test.csv', index=False) # give the file name

# Find the arduino serial port
ser = serial.Serial('COM6', 9600)
#time.sleep(2)
print(ser.name)

# Run the animation and show the figure
ani = FuncAnimation(fig, animation, frames=100, fargs=(data_list, ser, df), interval=100)
plt.show()

# after the window is closed, close the serial line
ser.close()
print("Serial line closed")

'''
# %%
