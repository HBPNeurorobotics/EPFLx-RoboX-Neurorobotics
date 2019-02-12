# class SARSA_evaluation 

import pandas as pd
import numpy as np
from matplotlib import collections as mc
from matplotlib import patches
import matplotlib.pyplot as plt
import random
import pylab as pl
from IPython import display
import math
import csv
import time

class SARSA_evaluation():
    
    def __init__(self):
        
        import warnings; warnings.filterwarnings('ignore')
        from SARSA_additional import SARSA_additional
        self.sarsaad = SARSA_additional()

        self.Nn = {}
        self.Q = {}
        self.actions = {}
        
        self.centers = {}
        self.edges = {}
            
    
	################################################################################
	# Modes
	################################################################################

    def run_evaluation(self,video):
		self.Nn,self.states,self.actions,self.reward,self.goal,self.Q = self.sarsaad.eva_analysis()
		self.M = self.perfect_map()
		self.video = video
		fastway = 0; longway = 0; neverway = 0; overway = 0

		for k in range(self.Nn):
			for h in range(self.Nn):
				self.start = [k,h]
				if(self.M[k,h]!=0.0):
					Qway = self.trial_evaluation()
					print "Number of steps:", len(self.X)
					print "Q-way:", ["%12.8f"% (q) for i,q in enumerate(Qway)]
					if(self.video): time.sleep(2)
					display.clear_output(wait=True)
					
					if   (len(Qway) == self.Nn*self.Nn): neverway += 1
					elif (len(Qway) == self.M[k,h]): fastway += 1
					else: longway += 1; overway += len(Qway) - self.M[k,h]
		return fastway, longway, overway, neverway




    def test_generation(self, start=None):
		self.Nn,self.states,self.actions,self.reward,self.goal,self.Q = self.sarsaad.eva_analysis()
		self.M = self.perfect_map()
		self.video = 1
		
		if(start==None): self.start = [np.random.randint(self.Nn),np.random.randint(self.Nn)]
		else: self.start = start

		while(self.M[self.start[0],self.start[1]] == 0):
			self.start = [np.random.randint(self.Nn),np.random.randint(self.Nn)]

		Qway = self.trial_evaluation()
		print "Number of steps:", len(self.X)
		print "Q-way:", ["%12.8f"% (q) for i,q in enumerate(Qway)]
		display.clear_output(wait=True)
		print "Number of steps:", len(self.X)
		self.Way = np.column_stack((self.X, self.Y))
		print np.transpose(self.Way)

		with open('SARSA_data_way_points.csv', 'w') as f:
			writer = csv.writer(f)
			writer.writerow(['x', 'y'])
			for i in range(len(self.X)):
				writer.writerow([self.X[i], self.Y[i]])
		
    
    def auto_generation(self):
		self.Nn,self.states,self.actions,self.reward,self.goal,self.Q = self.sarsaad.eva_analysis()
		self.M = self.perfect_map()
		return self.M


	################################################################################
	# additional to Modes
	################################################################################

    def trial_evaluation(self):
        Qway = []
        state = [self.start[0],self.start[1]]
        self.X = [self.start[0]]; self.Y = [self.start[1]];

        while(state != self.goal) and (len(Qway) < self.Nn*self.Nn):

            index = np.argmax(self.Q[state[0],state[1],:])
            Qway.append(self.Q[state[0],state[1],index])
            if  (index == 0): state[0] += 1
            elif(index == 1): state[0] -= 1
            elif(index == 2): state[1] += 1
            else:             state[1] -= 1

            self.X.append(state[0]); self.Y.append(state[1])
            if(self.video): self.visualizationE(self.states,self.actions)
        return Qway


    def perfect_map(self):
		N = self.Nn*self.Nn-1
		M = np.zeros((self.Nn,self.Nn))+100
		M[self.goal[0],self.goal[1]] = -1
		t = 0; L = 0
		while N > L:
			t += 1
			for i in range(self.Nn):
				for j in range(self.Nn):
				    ways = []
				    try: ways.append(self.reward[i+1,j,1])
				    except: n = 1
				    try: ways.append(self.reward[i-1,j,0]) 
				    except: n = 1
				    try: ways.append(self.reward[i,j+1,3])
				    except: n = 1
				    try: ways.append(self.reward[i,j-1,2])
				    except: n = 1

				    if(np.max(ways) < 0) and (t==1): L += 1
				    for d in range(4):
				        if(self.reward[i,j,d] == 1):
				            if(M[i,j]==100): N = N - 1
				            M[i,j] = 1; 
				        elif(self.reward[i,j,d] == 0):     
				            if(d==0):
				                if(M[i+1,j]+1<M[i,j]): 
				                    if(M[i,j]==100): N = N - 1
				                    M[i,j] = M[i+1,j] + 1;
				            if(d==1):
				                if(M[i-1,j]+1<M[i,j]): 
				                    if(M[i,j]==100): N = N - 1
				                    M[i,j] = M[i-1,j] + 1;
				            if(d==2):
				                if(M[i,j+1]+1<M[i,j]): 
				                    if(M[i,j]==100): N = N - 1
				                    M[i,j] = M[i,j+1] + 1; 
				            if(d==3):
				                if(M[i,j-1]+1<M[i,j]): 
				                    if(M[i,j]==100): N = N - 1
				                    M[i,j] = M[i,j-1] + 1; 


		M[self.goal[0],self.goal[1]] = 100
		self.M = np.where(M==100, 0, M)
		return self.M


	################################################################################
	# visualization
	################################################################################


    def visualizationE(self,states,actions):

        get_ipython().run_line_magic('matplotlib', 'inline')

        rect1 = patches.Rectangle((self.goal[1]-0.5,self.goal[0]-0.5), 1., 1., color='lime')
        rect2 = patches.Rectangle((self.start[1]-0.5,self.start[0]-0.5), 1., 1., color='orange')

        plt.figure(figsize=(8,6))
        im = plt.imshow(np.reshape(np.zeros(self.Nn*self.Nn), newshape=(self.Nn,self.Nn)),
                            interpolation='none', alpha=0.0, vmin=0, vmax=1, aspect='equal');

        ax = plt.gca();
        ax = plt.gca();
			
        idx = 0
        for i in range(self.Nn):
            for j in range(self.Nn):
                if i > 0:
                    if(self.actions[idx]):
                        x1 = (i-1)+0.5; y1 = (j)+0.5;
                        x2 = (i)-0.5;   y2 = (j)-0.5;
                        ax.plot([y1,y2],[x1,x2],'k',linestyle='-', linewidth=3)
                    idx += 1
                if j > 0:
                    if(self.actions[idx]):
                        x1 = (i)+0.5;   y1 = (j-1)+0.5;
                        x2 = (i)-0.5;   y2 = (j)-0.5;
                        ax.plot([y1,y2],[x1,x2],'k',linestyle='-', linewidth=3)
                    idx += 1


        for i in range(self.Nn):
            for j in range(self.Nn):
                if(states[self.Nn*i+j] == 0.0): 
                    rectB = patches.Rectangle((j-0.5, i-0.5), 1.0, 1.0, color='black')
                    ax.add_patch(rectB)


        ax.set_xlim(-0.5, self.Nn-0.5)
        ax.set_ylim(-0.5, self.Nn-0.5)
        ax.invert_yaxis()


        ax.add_patch(rect1)
        ax.add_patch(rect2)

        for hi in range(len(self.X)):
            rect = patches.Rectangle((self.Y[hi]-0.25,self.X[hi]-0.25),\
												0.5, 0.5, color='red', alpha=0.05+hi*0.04)
            ax.add_patch(rect)

        # Major ticks
        ax.set_xticks(np.arange(0, self.Nn, 1));
        ax.set_yticks(np.arange(0, self.Nn, 1));

        # Labels for major ticks
        ax.set_xticklabels(np.arange(0, self.Nn, 1));
        ax.set_yticklabels(np.arange(0, self.Nn, 1));

        # Minor ticks
        ax.set_xticks(np.arange(-.5, self.Nn, 1), minor=True);
        ax.set_yticks(np.arange(-.5, self.Nn, 1), minor=True);

        # --- Gridlines based on minor ticks
        ax.grid(which='minor', color='k', alpha = 0.2, linestyle='-', linewidth=1)

        # Gridlines based on minor ticks
        display.clear_output(wait=True)
        display.display(plt.gcf())
