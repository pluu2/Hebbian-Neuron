# -*- coding: utf-8 -*-
"""HebbianNeuron.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ErW6_iMc76zvDVAtls-EVXMgtU8w39h8
"""

import numpy as np
from sklearn.metrics import mean_squared_error 
import random
import matplotlib.pyplot as py


#documentation incomplete.

#hebbianNeuron, a neuron with many input, with single output of a single learned type. 
#beta = the rate of weight decay 
#max_decay = the iterations resulting in no more changes to weights
#alpha = the rate of reenforcement. 


#functions: 
#store_receivedID = stores the connections that the neuron forms with the previous layers. 
#store_sendID = stores the neuronconnection the neuron is sending signal to. 
#store pattern = the neuron stores a pattern, this pattern will be used to determine if the neuron will fire or not. 
#'output' this takes the input of a pattern, and then determines using MSE whether or not to fire. Remember the weight will decay each iteration. 


class hebbianNeuron():
#input dimensions is number of inputs, outputs is number of outputs of this single neuron
  def __init__(self, input_numbers=35,beta=0.1,max_decay = 5,alpha = 0.1): #all on intiiation 

    self.input_numbers=input_numbers
    #Outputs will be limited to 1
    iteration_time =0
    #the rate of reenformcenet
    self.alpha= alpha
    self.max_decay = max_decay
    #iteration time 
    self.iteration_time = iteration_time
    #this is the rate of decay of output connection 
    self.beta=beta
    #This is weight of the output 
    self.w =  1.0
    #This 'ID' represent the value that the connect the neuron forms with the next neuron over 
    self.sendID = 0
    self.receiveID = 0
    self.pattern=[]
    self.sensitivity=0.05

  def set_sensitivity (self,sensitivity_):
    self.sensitivity=sensitivity_

  #manifest will store which connections that the neuron will receive,  once this is assigned the neurons cannot receive additional ID.
  def store_receiveID (self,connections,override=False): 
    if self.receiveID==0 or override==True:
      self.receiveID = connections 
   #this will represent the connection number relative to the ENTIRE LAYER. 
  def store_sendID(self, ID): 
    self.sendID = ID 
  
  #this will store the pattern in which the neuron will respond to
  def store_pattern(self,pattern_,override=False):  #only new patterns assigned to neurons that do not have. 
    if self.pattern==[] or override==True:
      self.pattern = pattern_ 
   

  #I think what is missing is a way for the neurons to communicate. Maybe just a function. Cap at 1.0 weight
  def reward (self): 
    if self.iteration_time<=self.max_decay: #reward can only happen if the neuron has not decayed past max decay. 
      if self.w>1.0:
        self.w=1.0
      else:
       self.w=self.w +self.alpha 

    #I believe here under 'reward' the reward signal should propagate back to all connected neurons. 
    #I think in order to do this, a wrapper network will need to be done to trannsmit connections?
    return self.receiveID

  def decay(self):
    self.iteration_time +=1  
    if self.iteration_time <=self.max_decay:
      self.w = self.w-self.beta
 
  
  def output(self,inputs=1): #The 'class' is literally the connection weight no other calculation.  #call will generate the output.
    #This will load up the pattern that is stored, and compare it to the inputs.
    MSE = mean_squared_error (inputs, self.pattern) 
    if MSE <=self.sensitivity: #this is the threshold in which the neuron considers a pattern match . 
      return (1.0*self.w)
    else: 
      return (0.0) 

#------------------------------------------------------------------

class hebbianLayer (): 
  def __init__(self):
    self.neuron =[] #this will store the neurons. 
    self.inputVector=[] #the layer will store the input
    self.inputs=[]
    self.neuron_num=0
  def layer_input(self, inputVector_): 
    self.inputVector= inputVector_
    
  def add(self,neurons_=2,inputs_ = 5):  #will add number of neurons, with number of inputs , default is 2 neurons, with 5 inputs. 
    self.neuron_num+=neurons_ #store neurons
    self.inputs=inputs_ #store inputs 
    for i in range(neurons_): #this should only add what is specified. 
      self.neuron.append (hebbianNeuron(self.inputs)) #create 'neuron number', with 'input' inputs. 
    print ("Total number of Neurons: "  + str(self.neuron_num))
  
  def initialize(self,new_data=[],sense=0.05):
    if new_data==[]: 
      new_data=self.inputVector

    #initialize the neuron patterns for each neuron, and also initialize the connections. 
    #initializes connections 
    print ("Initializing.....")
    connections=[]
    for i in range (self.neuron_num):
      connections = random.sample (range(len(new_data)),self.inputs) #allocate a random subset of data but you do not want duplicates, draw from 5 points?
      self.neuron[i].store_receiveID(connections)
      self.neuron[i].set_sensitivity(sense)
    #assign pattern
      self.neuron[i].store_pattern (input_grouper(new_data,self.neuron[i].receiveID))
    print ("Done")

  def layer_output(self,input_response=[]): #default it goes with the original input vector, but ideally you want the input to be previous layer.
    #input vector to layer1
    if len(input_response)==0:
      input_response=self.inputVector

    output=[]
    for i in range(self.neuron_num):
      temp= self.neuron[i].output(np.array(input_grouper(input_response,self.neuron[i].receiveID))) #this grabs the data from the input vector to detect if pattern availab.e 
      output.append(temp)
      
    return output

  def decay (self): #decays all connections
    print ("Decaying all connections....")
    for i in range (self.neuron_num):
      self.neuron[i].decay()
    print ("Done")

  def reward(self,rewarded_neurons):  #reward all the appropriate neurons, then return a list of all connections these neurons connected to without duplicates?
    connections=[]
    for i in range(len(rewarded_neurons)):
      temp_connections = self.neuron[rewarded_neurons[i]].reward()
      connections.append(temp_connections)
    one_connection= np.concatenate(connections, axis=0) #this is done because the outut is a list of array. Now you got to find the reepating numbers
    output_connection= list(set(one_connection)) #remove duplicates. DONE.
    return output_connection


  def reshuffle(self): #this is neccessary when new neurons are added and you want to reshuffle the last layer to include connections from new neurons
    #initialize the neuron patterns for each neuron, and also initialize the connections. 
    #initializes connections 
    print ("Reshuffling")
    connections=[]
    for i in range (self.neuron_num):
      connections = random.sample (range(len(self.inputVector)),self.inputs) #allocate a random subset of data but you do not want duplicates, draw from 5 points?
      self.neuron[i].store_receiveID(connections,override=True)
    #assign pattern
      self.neuron[i].store_pattern (input_grouper(self.inputVector,self.neuron[i].receiveID),override=True)
    print ("Done")

#----------------------------------------------


def input_grouper(layer,connections):
  temp = [layer[i] for i in (connections)]
  return temp

#-----------------------------------------------
def hebLoss (layer,realoutput): 

  reward =[]
  for j in range(0,len(layer)):
   
    if layer[j]<realoutput[j]: #if neuron is not active when it is supposed to be 0 
      reward.append(j)
      #print ('reward')
  if len(reward)==0: 
    return -1
  else:
    return reward