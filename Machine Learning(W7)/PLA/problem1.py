# Artifical Intelligence @ edX
# Week7 Project Problem 1
# Perceptron Learning Algorithm
# Renjie Li, rl2932@columbia.edu

import numpy
import sys
import matplotlib.pyplot as plt


class PLA(object):

    def __init__(self):
        self.ori_data = numpy.genfromtxt(sys.argv[1], delimiter=",") # data from input
        self.output_name = sys.argv[2] # desired output name, in this case is output1.csv
        self.example_num = len(self.ori_data) # Number of examples
        self.f1 = self.ori_data[:,0] # feature 1
        self.f2 = self.ori_data[:,1] # feature 2
        self.x = numpy.array([self.f1,self.f2,numpy.ones(self.example_num),]).transpose() # 3rd column for w_0
        self.label = self.ori_data[:,2] # label, which is yi in pseudocode
        self.weights = [] # a list that stores the weights
        self.training()

    def training(self):
        self.w = numpy.zeros(3) # w_1,w_2 and b (aka w_0), though it looks ambiguous
        self.cache = numpy.ones(3) # an array that stores the previous weight set
        while not (self.w == self.cache).all() : # Repeat Until Convergence
            self.cache = self.w.copy() # Update the cache
            for i,xi in enumerate(self.x):
                if self.label[i] * numpy.sum(self.w*xi) <=0:
                    self.w += self.label[i] * xi
            self.weights.append(self.w.copy())
        self.weights = numpy.asarray(self.weights)
        numpy.savetxt('output1.csv',self.weights,fmt='%1.0f',delimiter=',')
        #self.plot()


    def plot(self):
        plt.figure()
        #plt.scatter(self.f1,self.f2,c=['blue','red'])
        plt.plot(self.ori_data[self.label==1.0,0],self.ori_data[self.label==1.0,1],'ro')
        plt.plot(self.ori_data[self.label==-1.0,0],self.ori_data[self.label==-1.0,1],'bo')
        xaxis = numpy.linspace(0,15,100)
        yaxis = -self.w[0] / self.w[1] * xaxis - self.w[2] / self.w[1]
        plt.plot(xaxis,yaxis,color='green')
        plt.show()



if __name__ == "__main__":
    Perceptron = PLA()