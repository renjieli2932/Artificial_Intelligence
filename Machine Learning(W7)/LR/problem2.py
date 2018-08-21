# Artifical Intelligence @ edX
# Week7 Project Problem 2
# Linear Regression
# Renjie Li, rl2932@columbia.edu
import numpy
import sys

class LR(object):

    def __init__(self):
        self.ori_data = numpy.genfromtxt(sys.argv[1], delimiter=",")  # data from input
        self.output_name = sys.argv[2]  # desired output name, in this case is output2.csv
        self.example_number = len(self.ori_data)
        self.age = (self.ori_data[:,0] - numpy.mean(self.ori_data[:,0]) ) / numpy.std(self.ori_data[:,0]) # Normalization
        self.weight = (self.ori_data[:,1] - numpy.mean(self.ori_data[:,1]) ) / numpy.std(self.ori_data[:,1])
        self.data = numpy.array([numpy.ones(self.example_number),self.age,self.weight]).transpose()
        self.label = self.ori_data[:,2] # Heights
        self.output = [] # store the output data
        self.GD() # Gradient Descent

    def GD(self):
        learn_rate = numpy.array([0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10,0.314])
        iterations = 100
        for alpha in learn_rate:
            b = numpy.zeros(3) # b_0,b_age,b_weight
            for iter in range(iterations):
                inbracket = numpy.sum(b*self.data,axis=1) -self.label
                result = 1.0 * numpy.dot(inbracket,self.data) * alpha / self.example_number
                b -= result
            param = numpy.array([alpha,iterations,b[0],b[1],b[2]])
            self.output.append(param)
        self.output = numpy.asarray(self.output)
        numpy.savetxt(self.output_name,self.output,delimiter=',')



if __name__ == "__main__":
    LinearRegression = LR()