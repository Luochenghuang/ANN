
import numpy
import matplotlib.pyplot
# scipy.sepcial or the sigmoid function expit()
import scipy.special

#image recog
import scipy.misc

import csv


numpy.set_printoptions(precision=10)



data_file = open("iris.data",'r')
data_list = data_file.readlines()
data_file.close()



#dataSanitizer cleans up data into learnable data
class dataSanitizer:
    
    # initialise the sanitizer
    def __init__(self, datalist, number_of_para, index_for_continuous, target_position):
        
        # initialize the datalist, keys, and index
        self.target_pos = target_position
        self.raw_data = datalist
        self.conti_index = index_for_continuous
        # a list of list
        self.keys = [[] for i in range(number_of_para + 1)]
        #the max of each continuous value
        self.conti_max = numpy.zeros(number_of_para) + 1
        self.data_points = len(datalist)
        self.starting_point = [[] for i in range(number_of_para + 1)]
        self.para = number_of_para
        self.new_data = []
        pass
    
    # define clean()
    def sort(self):
        
        # go through all records 
        for record in self.raw_data:
            # split the record by the ',' commas
            all_value = record.split(',')
            # if the label is new add to the self.keys

            for i, value in enumerate(all_value):
                #check if it's the target position
                if i == self.target_pos:
                    pass
                #update the max of continuous var
                elif i in self.conti_index:
                    value = float(value)
                    self.conti_max[i] = max(self.conti_max[i], value)
                    self.keys[i]=['']
                #update keys
                elif value not in self.keys[i]:
                    self.keys[i].append(value)
                    pass
                
            pass
        
        #update starting point
        elements = numpy.zeros(self.para)
        self.starting_point[0] = 0        

        for i in range(1,self.para+1):
            self.starting_point[i] = len(self.keys[i-1]) + self.starting_point[i-1]
            pass
        
        #number of labels
        length = 0
        for a in d.keys:
            length += len(a)
            
        #create a new array
        self.new_data = [[0 for i in range(length + 1)] for i in range(self.data_points + 1)]
    
    #transforms into useful data
    def binary_transform(self):
        
        
        # go through all records 
        for row, record in enumerate(self.raw_data):
            # split the record by the ',' commas
            all_value = record.split(',')
            # if the label is new add to the self.keys

            for i, value in enumerate(all_value):
                #update the max of continuous var
                if i == self.target_pos:
                    pass
                
                elif i in self.conti_index:
                    position = self.starting_point[i] 
                    self.new_data[row][position] = float(value)/self.conti_max[i]
                    pass
                

                #update keysv
                else:  
                    position = self.starting_point[i] + self.keys[i].index(value)
                    self.new_data[row][position] = 1
                    pass
                    
            pass
        return self.new_data
    
#puts the target value in front of each record
    def target_transform(self, dictionary):
        
        # go through all records 
        for row, record in enumerate(self.raw_data):
            # split the record by the ',' commas
            all_value = record.split(',')
            # if the target value matches in the dictionary
            if all_value[self.target_pos] in dictionary:
                self.new_data[row][self.starting_point[self.target_pos]] = dictionary[all_value[self.target_pos]]
            else:
                print("error locating target")
                print("Could not find", all_value[self.target_pos], "in dictionary.")
                pass
            pass
        pass


d = dataSanitizer(data_list, 4, [0,1,2,3],4)
d.sort()


print(d.keys)
d.target_transform({'Iris-setosa\n':0, 'Iris-versicolor\n':1, 'Iris-virginica\n':2,'Iris-virginica':2})


new = d.binary_transform()

data = numpy.asarray(new)

numpy.savetxt('sanitized_data', data, delimiter=',')

print(len(data[0]))