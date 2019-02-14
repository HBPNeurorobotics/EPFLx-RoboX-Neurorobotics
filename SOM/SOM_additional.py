# class SOM (SOM_solution)

import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.pyplot as plt

from matplotlib import collections as mc
from matplotlib import patches
from IPython import display
from IPython import get_ipython


class SOM_additional():

	# Self-Organizing Map mapping the environment depending on the positions visited by the robot
    
	def __init__(self):
		self.pos = {}
		import warnings; warnings.filterwarnings('ignore')



	#########################
	###   Visualization   ###
	#########################
    
	def visualization(self,lattice,Nn,eta,sigma,trial):
		# Self Organazing Map - Process visualization
		get_ipython().run_line_magic('matplotlib', 'inline')
    
		# SOM-MAP: centers and edges    
		edges = [] # list of links between centers
		centers = [] # list of centers
		for i in range(Nn):
			for j in range(Nn):
				if i > 0:
					edges.append([(lattice[i-1,j,0], lattice[i-1,j,1]),
                                  (lattice[i,j,0], lattice[i,j,1])])
				if j > 0:
					edges.append([(lattice[i,j-1,0], lattice[i,j-1,1]),
                                      (lattice[i,j,0], lattice[i,j,1])])

				centers.append((lattice[i,j,0],lattice[i,j,1]))
                
		Cx,Cy = zip(*centers)
		lc2 = mc.LineCollection(edges, colors='red', linewidths=.8)

		# ENVIRONMENT   
		# walls
		borders = [[(4.8,4.8), (4.8,-4.8)], [(4.8,-4.8), (-4.8,-4.8)],
                  [(-4.8,-4.8), (-4.8,4.8)], [(-4.8,4.8), (4.8,4.8)]]
		lc1 = mc.LineCollection(borders, colors='black', linewidths=1)

		# obstracles
		rect1 = patches.Rectangle((-3.0,-1.0), 1., 2., color='black')
		rect2 = patches.Rectangle((-3.0,1.0), 3., 1., color='black')
		rect3 = patches.Rectangle((0.0,-2.0), 2., 1., color='black')
		rect4 = patches.Rectangle((2.0,-2.0), 1., 3., color='black')
		
		# PLOT
		fig = plt.figure(0,figsize=(8, 6))
		
		fig.suptitle('Trial: {} [sigma: {}, eta: {}]; Map: {}x{} (links:{})'.format(int(trial), round(sigma,3), round(eta,3), Nn, Nn, len(edges)))
		ax = fig.add_subplot(111)

		ax.add_patch(rect1)
		ax.add_patch(rect2)
		ax.add_patch(rect3)
		ax.add_patch(rect4)
		ax.add_collection(lc1)
		ax.add_collection(lc2)    

		plt.plot(self.pos[:,0], self.pos[:,1],'b.',alpha=0.1)
		plt.plot(Cx, Cy,'ro',markersize=8.0)

		plt.gca().set_aspect('equal', adjustable='box')
		display.clear_output(wait=True)
		display.display(plt.gcf())



    ##############################
	###   Load and Save data   ###
	##############################
    
	def load_data(self,csv_file):
		# exctract and transform data
		states = pd.read_csv(csv_file, delimiter=',',header=0).values
		positions = np.array([pd.to_numeric(states[:,0], errors='coerce'), pd.to_numeric(states[:,1], errors='coerce')]).T

		# Reduce the number of data points
		self.pos = positions[slice(0,positions.shape[0],(positions.shape[0]/1000)),:]
		#N = self.pos.shape[0]
		return self.pos
        
    
	def save_lattice(self,lattice):
		# convert it to stacked format using Pandas
		stacked = pd.Panel(lattice.swapaxes(1,2)).to_frame().stack().reset_index()
		stacked.columns = ['x', 'y', 'z', 'value']
		# save to disk
		stacked.to_csv('SOM_data_lattice.csv', index=False)
