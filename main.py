# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hxe7cGAMpXMyTym-CR-wagkNFV2fKxo4

Author : Swati Sajee Kumar
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

"""Read data file using pandas"""

data= pd.read_csv('wdbc.dataset',header=None)

"""Drop the column containg the Patient IDs which is the first column in the data file.
Also Map the string M and B to 1 and 0 respectiviely
"""

data = data.drop(0,1)
data[1] = data[1].map({'M':1,'B':0})

"""Normalize the data excluding the first column which says M or B (mapped to 0 or 1)."""

temp1 = data[1]
temp2= data.iloc[:,1:31]
data_norm= ((temp2-temp2.min())/(temp2.max()-temp2.min()))*20
data_norm[1]=data[1]
c= list(data_norm.columns)
c= c[-1:]+c[:-1]
data_norm = data_norm[c]

"""Now split the data into three sets: train, test and validaton
Initially divide the data into two set 80% train and 20% test. Later divide this 20% to 10% and 10% for test and validation.
"""

train,test=train_test_split(data_norm,test_size=0.2,random_state=3)
test,valid=train_test_split(test,test_size=0.5,random_state=1)

"""Convert the data into numpy array"""

x_train = np.asarray(train.loc[:,2:31])
y_train = np.asarray(train.loc[:,1])

x_test = np.asarray(test.loc[:,2:31])
y_test = np.asarray(test.loc[:,1])

x_valid = np.asarray(valid.loc[:,2:31])
y_valid = np.asarray(valid.loc[:,1])

#print(len(y_test))
#print(len(y_train))
#print(len(y_valid))

"""Use LogReg (Logistic Regression) function to train our model"""

def LogReg(x_train,y_train,iterate,lr):


  #intialize the weights and bias to zero
  
  #instead of taking transpose of weights later we have resized so as the number of rows in theta is equal to the number of columns in x_train
  theta1 = np.zeros(x_train.shape[1])   
  theta0 =0 
  
  loss_plot=[]

  # get the number of samples
  m = y_train.size
  
  # GRADIENT DESCENT Algorithm to repeatedly update the theta value

  for i in range(iterate):

    z= np.dot(x_train,theta1)                       #dot product of theta1 and x_train to calculate the sigmoid function
    
    sigma = 1/(1+np.exp(-z))                        # getting the sigmoid function 
    # print(sigma)
    
    grad_des = np.dot(x_train.T,(sigma-y_train))/m  # Get the partial differentiation of the cost function for all the m samples with respect to theta 
    
    theta1-=lr*grad_des                             #updating the theta value 
    
    if( i % 2000 ==0):                             
      
      z= np.dot(x_train,theta1)    
      sigma = 1/(1+np.exp(-z))
      loss = (-y_train * np.log(sigma) - (1 - y_train) * np.log(1 -sigma)).mean()    #Calculating the loss for every 2000 iterations so as to plot a graph for 5 set of values
      loss_plot.append(loss)
     
      
  dict = {"theta0":theta0,"theta1":theta1,"loss":loss,"loss_plot":loss_plot}      #store the values of updated weightsa nd loss function into dictonary
  
  return dict

# predict function to predict the y value for every data input x
def predict (data, theta0,theta1):

  m = data.shape[1]   #number of samples
  
  y_predict = np.zeros((1,m))  #initialising y_predict to zeros
  
  theta1 = theta1.reshape(data.shape[0],1) 
  #print(theta1)  
  
  z= np.dot(theta1.T, data)+theta0 #take the dot product to calculate z and find the sigmoid function
  sigma = 1/(1+np.exp(-z))
  
  y_scatter_plot = []
 # print(y_scatter_plot)
  patient_id = []
    
  for j in range (sigma.shape[1]):
    y_scatter_plot.append(sigma[0,j])
    patient_id.append(j)
  
  for i in range(sigma.shape[1]):
    if(sigma[0,i]<0.5):
      y_predict[0,i] = 0          #if the sigma or y is less than 0.5 , it is Benign      
    else:
      y_predict[0,i] = 1           #if the sigma or y is more than 0.5 ,then it is Malign 
 
 #************************************** Plot -1 **************************************************************************************
      
#   inorder to check if our test data has been divided accurately into malign or benign with respect to line 0.5 we can plot the sigma values
#   to plot the malign/benign vs patient_id where id is 1 to m , uncooment the below line also only call train set and with any one lr rate
  
#   plt.scatter(y_scatter_plot,patient_id)  
#   plt.title ('Malign/Benign vs Patient_ID')
#   plt.ylabel('Patients')
#   plt.xlabel('Malign/Benign')
#   # Customize the major grid
#   plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
#   # Customize the minor grid
#   plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    
  return y_predict

"""Now we write a function to calculate the Precision of Training, Testing and validation data set"""

def perf_measure(y_actual, predicted_train):
    TP = 0          #True Positive
    FP = 0          #False Positive
    TN = 0          #True Negative
    FN = 0          #False Negative

    for i in range(len(predicted_train)): 
        if y_actual[i]==predicted_train[i]==1:
           TP += 1
        if predicted_train[i]==1 and y_actual[i]!=predicted_train[i]:
           FP += 1
        if y_actual[i]==predicted_train[i]==0:
           TN += 1
        if predicted_train[i]==0 and y_actual[i]!=predicted_train[i]:
           FN += 1
            
    return (TP,FP,TN,FN)

#create empty lists to store values of loss,updated weights, training accuracy , testing accuracy for every epoch
list_loss = [] 
weights = []
train_acc=[]
test_acc=[]
valid_acc=[]
loss_plot_list=[]
y_predict_test_list = []
y_predict_valid_list = []

num_iterations = [2000,4000,6000,8000,10000]

# The different values of Learning rates for which we test the model
#lr_list = [0.00004,0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008]

#The most accurate result for train set was obtained using lr = 0.0008 , thus just to check train accuracy TP, FP, TN and FN use the below lr list and comment out the above lr_list
lr_list = [0.0008]

for j in range (len(lr_list)):
  
  #Train our model for 10,000 iterations 
  epoch = LogReg(x_train,y_train,iterate = 10000, lr=lr_list[j])    
  loss = epoch["loss"]  
  theta1 = epoch["theta1"]
  theta0 = epoch["theta0"]
  loss_plot = epoch["loss_plot"]  
  
  # call the prediction model with the updated weights
  
  y_prediction_train = predict(x_train.T, theta0,theta1) 
  y_prediction_test= predict(x_test.T, theta0,theta1) 
  y_prediction_valid= predict(x_valid.T, theta0,theta1)  
  
  #**************************************************** Precision calculation for Training , Testing and Validation set *********************************************

  y_predic_test = [y for x in y_prediction_test for y in x]  
  
  TP,FP,TN,FN = perf_measure(y_test, y_predic_test)
  
  print('\n For Learning Rate equals : ' + str(lr_list[j]))
  print('\n True Positive for testing set is: '  + str(TP) )
  print('\n True Negative for testing set is: ' + str(TN))
  print('\n False Positive for testing set is: '  + str(FP))
  print('\n False Negative for testing set is: '  + str(FN))
  
  Accuracy = (TP +TN)/(TP+TN+FP+FN)
  Precision = (TP)/(TP+FP)
  Recall = (TP)/(TP+FN)
  
  print('\n Testing Accuracy is ' + ": {} %".format(Accuracy*100))
  print('\n Testing Precision is  ' +": {} %".format(Precision*100))
  print('\n Testing Recall is  ' + ": {} %".format(Recall*100))
  test_acc.append(Accuracy*100)                                       #Appends the accuracy of all lr's into test_acc list
  
  
  train_predic = [y for x in y_prediction_train for y in x]
  TP,FP,TN,FN = perf_measure(y_train, train_predic)
  train_a = (TP +TN)/(TP+TN+FP+FN)
  print('\n Training Accuracy is  ' + ": {} %".format(train_a*100))
  train_acc.append(train_a*100)                                       #Appends the accuracy of all lr's into train_acc list
  
  
  valid_predic = [y for x in y_prediction_valid for y in x]
  TP,FP,TN,FN = perf_measure(y_valid, valid_predic)
  valid_a = (TP +TN)/(TP+TN+FP+FN)
  print('\n Validation Accuracy is ' + ": {} %".format(valid_a*100))
  valid_acc.append(valid_a*100)                                        #Appends the accuracy of all lr's into train_acc list
  
 
  list_loss.append(loss)
  print("\n Loss Function is "+ ": {} %".format(loss*100) +"\n ----------------------------------------------------------" )
  
  weights.append(theta1)
  loss_plot_list.append(loss_plot)
  y_predict_test_list.append(y_prediction_test)
  y_predict_valid_list.append(y_prediction_valid)
  
  j=j+1



"""Plotting graphs. Uncomment the graph section when checking for the different values of lr list"""

# # Plot (1) Firstly for Learing Rate vs Testing Accuracy
# plt.plot (lr_list, test_acc) 
# #plt.grid()
# plt.title ('Learning Rate vs Testing Accuracy')
# plt.ylabel('Test accuracy')
# plt.xlabel('Learning Rate')
# plt.xticks(lr_list, rotation='vertical')
# plt.scatter(lr_list, test_acc)
# plt.minorticks_on()
# # Customize the major grid
# plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# # Customize the minor grid
# plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

# # Plot (2) Learing Rate vs Validation Accuracy
# plt.plot (lr_list, valid_acc) 
# #plt.grid()
# plt.title ('Learning Rate vs Validation Accuracy')
# plt.ylabel('Validation accuracy')
# plt.xlabel('Learning Rate')
# plt.xticks(lr_list, rotation='vertical')
# plt.scatter(lr_list, valid_acc)
# plt.minorticks_on()
# # Customize the major grid
# plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# # Customize the minor grid
# plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

# # Plot (3)  Learing Rate vs Training Accuracy
# plt.plot (lr_list, train_acc) 
# #plt.grid()
# plt.title ('Learning Rate vs Training Accuracy')
# plt.ylabel('Training accuracy')
# plt.xlabel('Learning Rate')
# plt.xticks(lr_list, rotation='vertical')
# plt.scatter(lr_list, train_acc)
# plt.minorticks_on()
# # Customize the major grid
# plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# # Customize the minor grid
# plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

# # Plot 4  Learing Rate vs Error function
# plt.plot (lr_list, list_loss) 

# #Title and labels
# plt.title ('Learning Rate vs Error Function')
# plt.ylabel('Error Function')
# plt.xlabel('Learning Rate')

# plt.xticks(lr_list, rotation='vertical')
# plt.scatter(lr_list, list_loss)
# plt.minorticks_on()

# # Customize the major grid
# plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# # Customize the minor grid
# plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

# # Plot 5   Error function vs Training Accuracy for different values of lr
# plt.scatter(list_loss, train_acc)
# plt.title ('Error Function vs Training Accuracy (for different values of lr)')
# plt.ylabel('Training Accuracy')
# plt.xlabel('Error Function')
# plt.minorticks_on()
# # Customize the major grid
# plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# # Customize the minor grid
# plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

# # Plot 6   Error function vs Testing Accuracy for different values of lr
# plt.scatter(list_loss, test_acc)
# plt.title ('Error Function vs Testing Accuracy (for different values of lr)')
# plt.ylabel('Testing Accuracy')
# plt.xlabel('Error Function')
# plt.minorticks_on()
# # Customize the major grid
# plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# # Customize the minor grid
# plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

# # Plot 7   Error function vs Validation Accuracy for different values of lr
# plt.scatter(list_loss, train_acc)
# plt.title ('Error Function vs Validation Accuracy (for different values of lr)')
# plt.ylabel('Validation Accuracy')
# plt.xlabel('Error Function')
# plt.minorticks_on()
# # Customize the major grid
# plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# # Customize the minor grid
# plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

# # Plot 9   Number of iterations vs Cost for every epoch
# plt.plot(num_iterations,loss_plot_list[0],'r', label ='lr = 0.00004')
# plt.plot(num_iterations,loss_plot_list[1],'black',label ='lr = 0.0002')
# plt.plot(num_iterations,loss_plot_list[2],'g',label ='lr = 0.0003')
# plt.plot(num_iterations,loss_plot_list[3],'y',label ='lr = 0.0004')
# plt.plot(num_iterations,loss_plot_list[4],'grey',label ='lr = 0.0006')
# plt.plot(num_iterations,loss_plot_list[5],'b--',label ='lr = 0.0008')

# plt.legend(loc='upper right');
# plt.title (' No. of iterations vs Cost')
# plt.ylabel('Cost')
# plt.xlabel('#iterations')

# plt.minorticks_on()

# # Customize the major grid
# plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# # Customize the minor grid
# plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

