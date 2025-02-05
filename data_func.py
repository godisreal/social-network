
#-----------------------------------------------------------------------
# Copyright (C) 2020, All rights reserved
#
# Peng Wang
#
#-----------------------------------------------------------------------
#=======================================================================
# 

# DESCRIPTION:
# This software is a python library for Opinion Simulation of Complex Social Interaction

# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@gmail.com

import sys, os
import pygame
import pygame.draw
import numpy as np
#from agent_model_obst3 import *
#from agent_model import *
#from obst import *
#from passage import *
#from math_func import *
from math import *
#from config import *
import re
import random
import csv
#from ctypes import *
import struct
import time
try:
    import matplotlib.pyplot as plt
except:
    print("Warning: matplotlib cannot be imported.  Unable to plot figures!")
    if sys.version_info[0] == 2: 
        raw_input("Please check!")
    else:
        input("please check!")


def readDoorProb(FileName, doorIndex, showdata=True):
    findMESH=False
    doorProb=[]
    for line in open(FileName):
        if re.match('&DoorProb', line):
            findMESH=True
            row=[]
        if  findMESH:
            if re.search('prob=', line):
                dataTemp=line.split('prob=')
                #print('dataTemp:', dataTemp[1:])

                #for index in range(len(dataTemp[1:])):
                #    probDist=dataTemp[index+1].lstrip('[').strip('=').rstrip(']')
                probDist=dataTemp[1].lstrip('[').strip('=').rstrip(']')
                temp2 =  re.split(r'[\s\,]+', probDist)
                print(temp2)
                prob = float(temp2[doorIndex+1].lstrip('[').strip('=').rstrip(']'))
                row.append(prob)
                #print(row)

                    #xpoints = temp2[0]
                    #ypoints = temp2[1]
            '''
            if re.search('XB', line):
                temp1=line.split('XB')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xmax = temp2[1]-temp2[0]
                ymax = temp2[3]-temp2[2]
            '''
            if re.search('WellDone!', line):
                findMESH = False
                #doorProb.append(dataTemp[1:])
                doorProb.append(row)
                # return xpoints, ypoints, xmax, ymax
                # Only find the first &MESH line
                # The second or other MESH lines are ignored

    print('doorProb', doorProb)
    (NRow, NColomn) = np.shape(doorProb)  
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = float(doorProb[i][j])
    print('matrix', matrix)
    if showdata:
        plt.plot(matrix)
        plt.grid()
        plt.show()
    return matrix


def readCSV_base(fileName):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)
    print(reader)
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    #print(strData)
    #print('np.shape(strData)=', np.shape(strData))
    #print('\n')

    print('\n')
    print('#=======================#')
    print(fileName)
    dataNP = np.array(strData)
    #print (dataNP)
    #print ('np.shape(dataNP)', np.shape(dataNP))
    #print ('\n')

    #print(strData[1:,1:])
    csvFile.close()
    return dataNP


def getData(fileName, strNote):
    dataFeatures = readCSV_base(fileName)

    Num_Data = len(dataFeatures)
    
    IPedStart=0
    Find = False
    #print(dataFeatures)
    for i in range(Num_Data):
        if len(dataFeatures[i]):
            if dataFeatures[i][0]==strNote:
                IPedStart=i
                Find = True
    
    if Find is False:
        return [], 0, 0
        #IPedStart = None
        #IPedEnd = None
        #dataOK = None
        #return dataOK, IPedStart, IPedEnd
        #return [], 0, 0
    else:
        IPedEnd=IPedStart
        for j in range(IPedStart, Num_Data):
            if len(dataFeatures[j]):
                if dataFeatures[j][0]=='' or dataFeatures[j][0]==' ':
                    IPedEnd=j
                    break
            else: #len(dataFeatures[j])==0: Namely dataFeatures[j]==[]
                IPedEnd=j
                break
            if j==Num_Data-1:
                IPedEnd=Num_Data

        dataOK = dataFeatures[IPedStart : IPedEnd]
        return dataOK, IPedStart, IPedEnd

    #data_result = np.array(dataOK)
    #return data_result[1:, 1:]
    

# This function is not used in this program
def readCSV(fileName, mode='float'):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    #print(strData)
    #print('np.shape(strData)=', np.shape(strData))
    #print('\n')

    print('\n')
    print('#=======================#')
    print(fileName)
    dataNP = np.array(strData)
    print (dataNP)
    print('np.shape(dataNP)', np.shape(dataNP))
    print('\n')

    #print(strData[1:,1:])
    csvFile.close()	
    
    if mode=='string':
        print (dataNP[1:, 1:])
        return dataNP[1:, 1:]
	
    if mode=='float':
        
        #print dataNP[1:, 1:]
        (I, J) = np.shape(dataNP)
        #print "The size of tha above matrix:", [I, J]
        #print "The effective data size:", [I-1, J-1]
        matrix = np.zeros((I, J))
        #print matrix

        for i in range(1,I):
            for j in range(1,J):
                matrix[i,j] = float(dataNP[i,j])

    print (matrix[1:, 1:])
    return matrix[1:, 1:]
    

def arr1D_2D(data, debug=True):
    #data is in type of 1D array, but it is actually a 2D data format.  
    
    NRow = len(data)
    NColomn = len(data[1])
    matrix = np.zeros((NRow, NColomn), dtype='|S20')
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = data[i][j]
    if debug:
        print('Data in 2D array:\n', matrix)
        
    return matrix


def readFloatArray(tableFeatures, NRow, NColomn, debug=True):

    #tableFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Ped2Exit')
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = float(tableFeatures[i+1][j+1])
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrix)
    return matrix



def readGroupCABD(tableFeatures, NRow, NColomn, debug=True):

    # NRow and NColomn are the size of data to be extracted from tableFeatures
    matrixC = np.zeros((NRow, NColomn))
    matrixA = np.zeros((NRow, NColomn))
    matrixB = np.zeros((NRow, NColomn))
    matrixD = np.zeros((NRow, NColomn))
    
    for i in range(NRow):
        for j in range(NColomn):
            
            if tableFeatures[i+1][j+1] and tableFeatures[i+1][j+1] != '0':
                try:
                    #temp=re.split(r'[\s\/]+', tableFeatures[i+1][j+1])
                    temp=re.split(r'\s*[;\|\s]\s*', tableFeatures[i+1][j+1])
                    matrixC[i,j] = float(temp[0])
                    matrixA[i,j] = float(temp[1])
                    matrixB[i,j] = float(temp[2])
                    matrixD[i,j] = float(temp[3])
                except:
                    print("Error in reading group data!")
                    input("Please check!")
                    matrixC[i,j] = 0.0
                    matrixA[i,j] = 0.0
                    matrixB[i,j] = 0.0
                    matrixD[i,j] = 0.0
            else:
                matrixC[i,j] = 0.0
                matrixA[i,j] = 0.0
                matrixB[i,j] = 0.0
                matrixD[i,j] = 0.0
                
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrixC, matrixA, matrixB, matrixD)
    return matrixC, matrixA, matrixB, matrixD


def readGroupABD(tableFeatures, NRow, NColomn, debug=True):

    # NRow and NColomn are the size of data to be extracted from tableFeatures
    matrixA = np.zeros((NRow, NColomn))
    matrixB = np.zeros((NRow, NColomn))
    matrixD = np.zeros((NRow, NColomn))
    
    for i in range(NRow):
        for j in range(NColomn):
            
            if tableFeatures[i+1][j+1] and tableFeatures[i+1][j+1] != '0':
                try:
                    #temp=re.split(r'[\s\/]+', tableFeatures[i+1][j+1])
                    temp=re.split(r'\s*[;\|\s]\s*', tableFeatures[i+1][j+1])
                    matrixA[i,j] = float(temp[0])
                    matrixB[i,j] = float(temp[1])
                    matrixD[i,j] = float(temp[2])
                except:
                    print("Error in reading group data!")
                    input("Please check!")
                    matrixA[i,j] = 0.0
                    matrixB[i,j] = 0.0
                    matrixD[i,j] = 0.0
            else:
                matrixA[i,j] = 0.0
                matrixB[i,j] = 0.0
                matrixD[i,j] = 0.0
                
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrixA, matrixB, matrixD)
    return matrixA, matrixB, matrixD
    

def readGroupC(tableFeatures, NRow, NColomn, debug=True):
    # NRow and NColomn are the size of data to be extracted from tableFeatures
    matrixC = np.zeros((NRow, NColomn))
    if tableFeatures[i+1][j+1] and tableFeatures[i+1][j+1] != '0':
        try:    
            matrixC[i,j] = float(tableFeatures[i+1][j+1])        
        except:
            print("Error in reading group data!")
            input("Please check!")
            matrixC[i,j] = 0.0
    else:
        matrixC[i,j] = 0.0
                
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrixC)
    return matrixC

def readSocialArrayCSV(FileName, debug=True, marginTitle=1):

    #dataFeatures = readCSV_base(FileName)
    #[Num_Data, Num_Features] = np.shape(dataFeatures)   

    agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Ped')
    Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&agent')
        Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Agent')
        Num_Agents=len(agentFeatures)-marginTitle

    if debug: 
        print ('Number of Agents:', Num_Agents, '\n')
        print ("Features of Agents\n", agentFeatures, "\n")

    agent2exitFeatures, lowerIndex, upperIndex = getData(FileName, '&agent2exit')
    Num_Agent2Exit=len(agent2exitFeatures)-marginTitle
    if Num_Agent2Exit <= 0:
        agent2exitFeatures, lowerIndex, upperIndex = getData(FileName, '&ped2exit')
        Num_Agent2Exit=len(agent2exitFeatures)-marginTitle
    if Num_Agent2Exit <= 0:
        agent2exitFeatures, lowerIndex, upperIndex = getData(FileName, '&Ped2Exit')
        Num_Agent2Exit=len(agent2exitFeatures)-marginTitle
    if debug:
        print ('Number of Agent2Exit:', Num_Agent2Exit, '\n')
        print ('Features of Agent2Exit\n', agent2exitFeatures, "\n")

    agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupC')
    Num_AgentGroup=len(agentgroupFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupCABD')
        Num_AgentGroup=len(agent2exitFeatures)-marginTitle
    if Num_AgentGroup <= 0:
        agentgroupFeatures, lowerIndex, upperIndex = getData(FileName, '&groupABD')
        Num_AgentGroup=len(agent2exitFeatures)-marginTitle
    if debug:
        print ('Number of AgentGroup:', Num_AgentGroup, '\n')
        print ('Features of AgentGroup\n', agentgroupFeatures, "\n")

    '''
    obstFeatures, lowerIndex, upperIndex = getData(FileName, '&Wall')
    Num_Obsts=len(obstFeatures)-marginTitle
    if Num_Obsts <= 0:
        obstFeatures, lowerIndex, upperIndex = getData(FileName, '&wall')
        Num_Obsts=len(obstFeatures)-marginTitle

    if debug:
        print ('Number of Walls:', Num_Obsts, '\n')
        print ("Features of Walls\n", obstFeatures, "\n")

    exitFeatures, lowerIndex, upperIndex = getData(FileName, '&Exit')
    Num_Exits=len(exitFeatures)-marginTitle
    if Num_Exits <= 0:
        exitFeatures, lowerIndex, upperIndex = getData(FileName, '&exit')
        Num_Exits=len(exitFeatures)-marginTitle
        
    if debug: 
        print ('Number of Exits:', Num_Exits, '\n')
        print ("Features of Exits\n", exitFeatures, "\n")

    doorFeatures, lowerIndex, upperIndex = getData(FileName, '&Door')
    Num_Doors=len(doorFeatures)-marginTitle
    if Num_Doors <= 0:
        doorFeatures, lowerIndex, upperIndex = getData(FileName, '&door')
        Num_Doors=len(doorFeatures)-marginTitle
        
    if debug:
        print ('Number of Doors:', Num_Doors, '\n')
        print ('Features of Doors\n', doorFeatures, "\n")
        
    exit2doorFeatures, lowerIndex, upperIndex = getData(FileName, '&Exit2Door')
    Num_Exit2Door=len(exit2doorFeatures)-marginTitle
    if Num_Exit2Door <= 0:
        exit2doorFeatures, lowerIndex, upperIndex = getData(FileName, '&exit2door')
        Num_Exit2Door=len(doorFeatures)-marginTitle

    if debug:
        print ('Number of Exit2Door:', Num_Exit2Door, '\n')
        print ('Features of Exit2Door\n', exit2doorFeatures, "\n")
    '''

    return agentFeatures, agent2exitFeatures, agentgroupFeatures #, obstFeatures, exitFeatures, doorFeatures, exit2doorFeatures


'''
# The file to record the some output data of the simulation
# f = open("outData.txt", "w+")

def readAgents(FileName, debug=True, marginTitle=1, ini=1):

    #dataFeatures = readCSV_base(FileName)
    #[Num_Data, Num_Features] = np.shape(dataFeatures)   

    agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Ped')
    Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&agent')
        Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Agent')
        Num_Agents=len(agentFeatures)-marginTitle

    if debug: 
        print ('Number of Agents:', Num_Agents, '\n')
        print ("Features of Agents\n", agentFeatures, "\n")

    agents = []
    for agentFeature in agentFeatures[marginTitle:]:
        agent = person()
        agent.pos = np.array([float(agentFeature[ini+0]), float(agentFeature[ini+1])])
        agent.dest= np.array([float(agentFeature[ini+2]), float(agentFeature[ini+3])])
        agent.tau = float(agentFeature[ini+4])
        agent.tpre = float(agentFeature[ini+5])
        agent.p = float(agentFeature[ini+6])
        agent.pMode = agentFeature[ini+7]
        agent.aType = agentFeature[ini+8]
        agent.interactionRange = float(agentFeature[ini+9])
        agent.ID = int(agentFeature[ini+10])
        agent.moving_tau = float(agentFeature[ini+11])
        agent.tpre_tau = float(agentFeature[ini+12])
        agent.talk_tau = float(agentFeature[ini+13])
        agent.talk_prob = float(agentFeature[ini+14])
        agent.inComp = int(agentFeature[ini+15])
        agents.append(agent)
        
    return agents


##############################################
# This function will be used to read CHID from FDS input file
def readCHID(FileName):

    findHEAD=False
    for line in open(FileName):
        if re.match('&HEAD', line):
            findHEAD=True
        if  findHEAD:
            if re.search('CHID', line):
                temp1=line.split('CHID')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                keyInfo = temp2[0]
                return keyInfo
            if re.search('/', line):
                findHEAD = False
    return None

# Find the first &MESH line in FDS input file and return the value
def readMesh(FileName):
    findMESH=False
    for line in open(FileName):
        if re.match('&MESH', line):
            findMESH=True
        if  findMESH:
            if re.search('IJK', line):
                temp1=line.split('IJK')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xpoints = temp2[0]
                ypoints = temp2[1]
            if re.search('XB', line):
                temp1=line.split('XB')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xmax = temp2[1]-temp2[0]
                ymax = temp2[3]-temp2[2]
            if re.search('/', line):
                findMESH = False
                return xpoints, ypoints, xmax, ymax
                # Only find the first &MESH line
                # The second or other MESH lines are ignored
    return None


def readTEnd(FileName):
    
    findTIME=False
    for line in open(FileName):
        if re.match('&TIME', line):
            findTIME=True
        if  findTIME:
            if re.search('T_END', line):
                temp1=line.split('T_END')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                keyInfo = temp2[0]
                return keyInfo   # Return a string
            if re.search('/', line):
                findTIME = False
            
    keyInfo=0.0    #If T_END is not found, then return 0.0
    return keyInfo
    #return None
    

# To be added
def readKeyOnce(FileName, Title, Key):
    findTitle=False
    for line in open(FileName):
        if re.match(Title, line):
            findTitle=True
        if  findTitle:
            if re.search(Key, line):
                temp1=line.split(Key)
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                keyInfo = temp2[0]
                findTitle=False
                return keyInfo
            #if re.match(Title, line)==False and re.match('&', line):
            if re.search('/', line):
                findTitle = False
    return None

##############################################################
# The function writeFRec is modified from Topi's work
# python script: readFRec (by Topi on Google Forum)
# readFRec: Read fortran record, return payload as bytestring
##############################################################
#
def writeFRec(infile, fmt, data):
    len1 = np.size(data)
    if len1==0 or data is None:
        #len2=infile.read(4)
        #infile.write(0x00)
        temp = struct.pack('@I', 0)
        infile.write(temp)
    
        return None
    
    #if fmt=='s':
        #result  = struct.pack('@I', data.encode())
    #    infile.write(data.encode())
    # Not try data.encode().  Use standard format to write data
        
    fmt2 = str(len1)+fmt
    num  = len1 * struct.calcsize(fmt)
    
    # length of the data
    num2   = struct.pack('@I', num)
    infile.write(num2)
    
    # Modified on 2022 Apr2: Handle string type differently from int and float type
    if fmt=='s':
        result = struct.pack(fmt, data.encode())
        infile.write(result)
    
        # End symbol
        temp = struct.pack('@I', 0)
        infile.write(temp)
        return "write a string"

    # Write data
    for i in range(len1):
        result = struct.pack(fmt, data[i])
        infile.write(result)
    
    # End symbol
    temp = struct.pack('@I', 0)
    infile.write(temp)
    

    
#Read fortran record, return payload as bytestring
def readFRec(infile,fmt):
    len1   = infile.read(4)
    if not len1:
        return None
    len1   = struct.unpack('@I', len1)[0]

    if len1==0:
        len2=infile.read(4)
        return None
    num    = int(len1/struct.calcsize(fmt))
    fmt2   = str(num)+fmt
    if num>1:
        result = struct.unpack(fmt2,infile.read(len1))
    else:
        result = struct.unpack(fmt2,infile.read(len1))[0]
    len2   = struct.unpack('@I', infile.read(4))[0]
    if fmt == 's':
        result=result[0].rstrip()
    return result


def intiPrt(fileName, debug=True):
    
    n_part=1  # Number of PARTicle classes
    [n_quant,zero_int]=[6,0]  # Number of particle features
    
    #filename=open('test.bin', 'wb+')
    writeFRec(fileName, 'I', [1])      #! Integer 1 to check Endian-ness
    writeFRec(fileName, 'I', [653])    # FDS version number
    writeFRec(fileName, 'I', [n_part]) # Number of PARTicle classes
    for npc in range(n_part):
        writeFRec(fileName, 'I', [n_quant, zero_int])
        for nq in range(n_quant):
            if nq == 0:
                writeFRec(fileName,'s', "desired Vx") # smv_label
                writeFRec(fileName,'s', "m/s")        # units
                #q_units.append(units)  
                #q_labels.append(smv_label)
            if nq ==1:
                writeFRec(fileName,'s', "desired Vy") # smv_label
                writeFRec(fileName,'s', "m/s")        # units
                #q_units.append(units)  
                #q_labels.append(smv_label)
            if nq ==2:
                writeFRec(fileName,'s', "actual Vx") # smv_label
                writeFRec(fileName,'s', "m/s")        # units
            if nq ==3:
                writeFRec(fileName,'s', "actual Vy") # smv_label
                writeFRec(fileName,'s', "m/s") 
            if nq ==4:
                writeFRec(fileName,'s', "motive Fx") # smv_label
                writeFRec(fileName,'s', "N")        # units
            if nq ==5:
                writeFRec(fileName,'s', "motive Fy") # smv_label
                writeFRec(fileName,'s', "N")        # units
#            if nq ==6:
#                writeFRec(fileName,'s', "group Fx") # smv_label
#                writeFRec(fileName,'s', "N")        # units
#            if nq ==7:
#                writeFRec(fileName,'s', "group Fy") # smv_label
#                writeFRec(fileName,'s', "N")        # units            
                

#################################################
# This function is used to dump evac prt5 data file
# so that the simulation result can be visualized by smokeview
#################################################
def dump_evac(agents, fileName, T, debug=True):
    
    num = len(agents)
    
    x=[]
    y=[]
    z=[]
    ap1=[]
    ap2=[]
    ap3=[]
    ap4=[]
    
    tag=[]
    # n_quant = ?  Please revise in intiPrt()
    Q_desiredVx=[]
    Q_desiredVy=[]
    Q_actualVx=[]
    Q_actualVy=[]
    Q_motiveFx=[]
    Q_motiveFy=[]
    Q_groupFx=[]
    Q_groupFy=[]
    
    for agent in agents:
        if agent.inComp == 0:
            continue
        
        x.append(agent.pos[0])
        y.append(agent.pos[1])
        z.append(1.5)

        # 180* np.arctan2(agent.actualV[1], agent.actualV[0]) /pi
        #angle = vectorAng(agent.actualV)
        ap1.append(vectorAng(agent.actualV))        # velocity direction  Agent HR angle is [0,2PI)
        ap2.append(0.1)     # diameter
        ap3.append(0.05)    #torso diameter
        ap4.append(1.0)     # height
        
        tag.append(agent.ID)

        Q_desiredVx.append(agent.desiredV[0])
        Q_desiredVy.append(agent.desiredV[1])
        Q_actualVx.append(agent.actualV[0])
        Q_actualVy.append(agent.actualV[1])
        Q_motiveFx.append(agent.motiveF[0])
        Q_motiveFy.append(agent.motiveF[1])
        Q_groupFx.append(agent.groupF[0])
        Q_groupFy.append(agent.groupF[1])
        
        #self.groupF        
        #self.selfrepF
        
    NPLIM=np.size(tag)
    # ??? what happens if tag is an empty list
    # if tag is empty, do not write agent data to the binary file
    xyz=x+y+z+ap1+ap2+ap3+ap4
    # tag=tag  tag is already OK
    Q=Q_desiredVx+Q_desiredVy+Q_actualVx+Q_actualVy +Q_motiveFx+Q_motiveFy #+Q_groupFx+Q_groupFy

    writeFRec(fileName, 'f', [T])
    writeFRec(fileName, 'I', [NPLIM])
    if NPLIM>0:
        writeFRec(fileName, 'f', xyz)
        writeFRec(fileName, 'I', tag)
        writeFRec(fileName, 'f', Q)

'''

if __name__ == '__main__':

    test = readCSV_base(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    print(test)
    doorFeatures = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&Door')
    
    #print (doorFeatures)
    print (np.shape(doorFeatures))

    pedFeatures = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&Ped')
    #print (pedFeatures)
    print (np.shape(pedFeatures))

    agents = readAgents("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    walls = readWalls("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    doors = readDoors("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    exits = readExits("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    
    print ('Length of agents:', len(agents))
    print ('Length of walls:', len(walls))
    
    ped2ExitFeatures, LowerIndex, UpperIndex = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&Ped2Exit')
    #print (ped2ExitFeatures)
    matrix = np.zeros((len(agents), len(exits)))
    
    for i in range(len(agents)):
            for j in range(len(exits)):
                matrix[i,j] = float(ped2ExitFeatures[i+1][j+1])
    print ('matrix', matrix)

    #Exit2DoorFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Exit2Door')
    #print (Exit2DoorFeatures)
    #matrix = np.zeros((len(exits), len(doors)))
    #for i in range(len(exits)):
    #        for j in range(len(doors)):
    #            matrix[i,j] = float(Exit2DoorFeatures[i+1][j+1])
    #print ('matrix', matrix)
    
        #for index in range(Num_Data):
        #if dataFeatures[0,index]=='&Ped':
        #    IPedStart=index
        #    while dataFeatures[0,index]!='':
        #        index=index+1
        #    IPedEnd=index

    #agentFeatures = dataFeatures[IPedStart : IPedEnd]
    #[Num_Agents, Num_Features] = np.shape(agentFeatures)

    #doors = readDoors("doorData2019.csv", True)
    #exits = readExits("doorData2018.csv", True)
    
    # Initialize Desired Interpersonal Distance
    #DFactor_Init = readCSV("D_Data2018.csv", 'float')
    #AFactor_Init = readCSV("A_Data2018.csv", 'float')
    #BFactor_Init = readCSV("B_Data2018.csv", 'float')

    tableFeatures, LowerIndex, UpperIndex = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&groupB')
    BFactor_Init = readFloatArray(tableFeatures, len(agents), len(agents))
    BFactor_Init

    # Input Data Check
    #[Num_D1, Num_D2]=np.shape(DFactor_Init)
    #[Num_A1, Num_A2]=np.shape(AFactor_Init)
    #[Num_B1, Num_B2]=np.shape(BFactor_Init)

    #print >>f, np.shape(DFactor_Init), [Num_Agents, Num_Agents], '\n'

    print('\n', 'Test Output: exit2door.csv')
    exit2door=np.array([[ 1.0,  1.0,  1.0], [ 1.0,  -1.0,  -2.0], [ 1.0,  1.0,  1.0]])
    #print(exit2door)
    updateExit2Doors(exit2door, 'test_exit2door.csv')
    
    readDoorProb(r'/mnt/sda6/gitwork2022/CrowdEgress/examples/3Doors/ped2023Jan_2023-05-16_02_11_26.txt')
    
    
""" Test struct to read and write binary data
    n_part=2
    [n_quant,zero_int]=[1,0]
    f=open('test.bin', 'wb+')
    writeFRec(f, 'I', [1])      #! Integer 1 to check Endian-ness
    writeFRec(f, 'I', [653])    # FDS version number
    writeFRec(f, 'I', [n_part]) # Number of PARTicle classes
    for npc in range(n_part):
        writeFRec(f, 'I', [n_quant, zero_int])
        for nq in range(n_quant):
            smv_label =writeFRec(f,'s', "test")
            units     =writeFRec(f,'s', "Newton")
            #q_units.append(units)  
            #q_labels.append(smv_label)
    x1=[1.0, 2.0, 3.0]
    writeFRec(f, 'f', x1)
    x2=[1,2,3]
    writeFRec(f, 'I', x2)
    x3="abcdefg"
    writeFRec(f, 's', x3)
    f.close()
    
    f=open('test.bin', 'rb')
    testEnd =readFRec(f, 'I')
    ver =readFRec(f, 'I')
    n_part =readFRec(f, 'I')
    y1 = readFRec(f, 'f')
    y2 = readFRec(f, 'I')
    y3 = readFRec(f, 's') 
    print testEnd
    print ver
    print n_part
    print y1
    print y2
    print y3
    
"""
