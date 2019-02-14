#%%writefile SOM_Surname_Name.py 
# class SOM (SOM_solution)

import numpy as np
import random

from IPython import display



class SOM():

	# Self-Organizing Map mapping the environment depending on the positions visited by the robot
    
	def __init__(self, video=0, csv_file='test1_robot_position.csv'):
		# Inputs:
		#	 Nn: size of the 2D lattice (Nn*Nn)
		#	 eta: learning rate
		#	 sigma_0: initial width of the neighborhood function
		#	 tau_sigma: mean life time of width (decaying exponential)
		#	 sigma_min: width minimum value


		''' TO DO: set parameters of SOM training '''
		self.Nn = 4
		self.eta_0 = 1.0
		self.sigma_0 = 3.0
        
		self.eta_min = 0.001
		self.sigma_min = 0.0
        
		self.tau = 100.0
		''' --------------- TO DO --------------- '''
    

		self.pos = {}
		self.mix = {}
		self.trial = 0 # number of updates (eta and sigma can depend on the number of updates)
		self.video = video
		self.csv_file = csv_file
        
		# Lattice of neurons (SOM) of size [Nn,Nn]. The third dimension allows to store x and y coordinates.
		# The values are randomly initialized
		self.lattice = np.random.uniform(0.,1.0,(self.Nn,self.Nn,2))
        

    
    
	### Run simulation (main function) ###
        
	def run_som(self):
		'''----- Additional functions: upload, visualize, save ----- '''
		from SOM_additional import SOM_additional
		somad = SOM_additional() 
		'''--------------------------------------------------------- '''
        
		self.pos = somad.load_data(self.csv_file)
		while(self.trial < self.tau):
			self.run_trial()
			somad.save_lattice(self.lattice)
			if(self.video): somad.visualization(self.lattice,self.Nn,self.eta(),self.sigma(),self.trial)
			self.trial += 1
		display.clear_output(wait=True)



	### SOM training stages ###

	def run_trial(self):
		self.mix = self.datamix();
		for i in range(self.pos.shape[0]):
			self.run_episode(i)


	def run_episode(self,i):
		pt = self.pos[self.mix[i]] 
		d = self.distance(pt)
		[lx,ly] = self.winner(d)
		h = self.neighborhood_factor(lx[0],ly[0])
		self.update_lattice(h,pt)


	def update_lattice(self,h,pt):
		for i in range(self.lattice.shape[2]):
			self.lattice[:,:,i] += self.eta()*h*((pt-self.lattice)[:,:,i])



	### Neighborhood factor ###
        
	def distance(self, pt):
		return np.linalg.norm(self.lattice - pt,axis=2)**2
    
    
	def winner(self,d):
		return np.where(d == d.min())
        
    
	def neighborhood_factor(self,lx,ly):
		h = np.zeros((self.Nn,self.Nn))
		for i in range(self.Nn):
			for j in range(self.Nn):
				dist = (i-lx)**2 + (j-ly)**2
				h[i,j] = np.exp(-dist/(2*self.sigma()**2))
		return h



	### Parameters ###
        
	def eta(self):
		return self.eta_0*(1-self.trial/self.tau)
    
    
	def sigma(self):
		return self.sigma_0*(1-self.trial/self.tau)
        
        
	def datamix(self):
		mix = []
		for j in range(self.pos.shape[0]):
			mix.append(random.randint(0,self.pos.shape[0]-1))
		return mix
