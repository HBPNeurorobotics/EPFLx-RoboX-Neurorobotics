# class SOM_evaluation

import pandas as pd
import numpy as np
import math
import csv


class SOM_evaluation():
    
    def __init__(self):
    
        self.Nn = {}
        self.lattice = {}
        self.pos = {}
        import warnings; warnings.filterwarnings('ignore')

        
    def run_evaluation(self):
        self.load_lattice()
        var = self.variation()
        return var, self.Nn
        
        
    def variation(self):
        
        var = np.zeros((self.Nn,self.Nn))
        nvar = np.zeros((self.Nn,self.Nn))
        for i in range(self.pos.shape[0]):
            pt = self.pos[i]

            d = np.linalg.norm(self.lattice - pt,axis=2)**2
            (lx,ly) = np.where(d == d.min())

            var[lx,ly]  += d.min()
            nvar[lx,ly] += 1

        for i in range(self.Nn):
            for j in range(self.Nn):
                if(nvar[i,j] > 0.0):
                    var[i,j] = var[i,j]/nvar[i,j]

        return sum(sum(var))/self.Nn**2
    

    
    def load_lattice(self):
        # exctract and transform data
        states = pd.read_csv('NRP_data_robot_positions.csv', delimiter=',',header=0).values
        positions = np.array([pd.to_numeric(states[:,0], errors='coerce'), pd.to_numeric(states[:,1], errors='coerce')]).T
        # Reduce the number of data points
        self.pos = positions[slice(0,positions.shape[0],1000),:]
        N = self.pos.shape[0]

        # load data of som-lattice from csv 
        with open("SOM_data_lattice.csv") as f:
            reader = csv.reader(f)
            next(reader) # skip header
            data = [r for r in reader]
        # calculate Nn
        self.Nn = int(math.sqrt(len(data)/2))
        # re-create lattice
        self.lattice = np.zeros((self.Nn,self.Nn,2))
        for i,line in enumerate(data):
            z = line[0]; y = line[1]; x = line[2];
            self.lattice[x,y,z] = line[3]
