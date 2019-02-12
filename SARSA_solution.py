#%%writefile SARSA_Surname_Name.py 
# class SARSA (Sarsa_solution)
                                                                                               
import numpy
import time
from pylab import *
import matplotlib.pyplot as plt


class SARSA_solution:
    """
    A class that implements a quadratic NxN gridworld. 
    
    Methods:
    
    learn(N_trials=100):	Run 'N_trials' trials. 
							A trial is finished, when the agent reaches the reward location.
    visualize_trial()  : 	Run a single trial with graphical output.
    reset()            : 	Make the agent forget everything he has learned.
    plot_Q()           : 	Plot of the Q-values .
    learning_curve()   : 	Plot the time it takes the agent to reach the target 
							as a function of trial number. 
    navigation_map()   : 	Plot the movement direction with the highest Q-value for all positions.
    """    
        
    def __init__(self):
        from SARSA_additional import SARSA_additional
        self.sarsaad = SARSA_additional()
        """
        Creates a quadratic NxN gridworld. 

        Mandatory argument:
        N: size of the gridworld

        Optional arguments:
        reward_position = (x_coordinate,y_coordinate): the reward location
        obstacle = True:  Add a wall to the gridworld.
        
        reward_position,obstacle=False, lambda_eligibility=0.2
        """    
        
        # gridworld size
        self.pos = self.sarsaad.upload_positions()#(self)pos
        self.lattice = self.sarsaad.upload_lattice()#(self)lattice
        self.Nn = len(self.lattice[0])
        self.Reward, self.reward_position = self.sarsaad.upload_reward()#(self)Reward
        
        
        self.centers = {}
        self.edges = {}
        self.video = {}
              

        # reward administered t the target location and when
        # bumping into walls
        self.reward_at_target = 1.
        self.reward_at_wall   = -0.5
        
        self.Trial = 0
        self.Run = 0
        self.N_trials = 3000
        

        # probability at which the agent chooses a random
        # action. This makes sure the agent explores the grid.
        self.epsilon = 0.9
                                                                                                  
        # learning rate
        self.eta = 0.9

        # discount factor - quantifies how far into the future
        # a reward is still considered important for the
        # current action
        self.gamma = 0.5

        # the decay factor for the eligibility trace the
        # default is 0., which corresponds to no eligibility
        # trace at all.
        self.lambda_eligibility = 0.2
    
        # is there an obstacle in the room?
        #self.obstacle = obstacle

        # initialize the Q-values etc.
        self._init_run()





    def run(self,video):
        #print "run"
        self.video = video
        self.latencies = zeros(self.N_trials)
        self.tau = self.N_trials/4
        
        #for run in range(N_runs):
        self._init_run()
        #call reset() to reset Q-values and latencies, ie forget all he learnt 
        #self.reset()
        latencies = self._learn_run()
        self.latencies += latencies/self.N_trials
        
        
        #self.getQvalue()
        self.sarsaad.save_Qvalue(self.Q)
        self.sarsaad.print_Qvalue(self.Q)

    
    ###############################################################################################
    # The remainder of methods is for internal use and only relevant to those of you
    # that are interested in the implementation details
    ###############################################################################################
        
    
    def _init_run(self):
        #print "_init_run"
        
        #Initialize the Q-values, eligibility trace, position etc.
        
        # initialize the Q-values and the eligibility trace
        self.Q = 0.01 * numpy.random.rand(self.Nn,self.Nn,4) + 0.1
        self.e = numpy.zeros((self.Nn,self.Nn,4))
        
        # list that contains the times it took the agent to reach the target for all trials
        # serves to track the progress of learning
        self.latency_list = []

        # initialize the state and action variables
        self.x_position = None
        self.y_position = None
        self.action = None
    
    def _learn_run(self):
        #print "_learn_run"
        
        #Run a learning period consisting of N_trials trials. 
        
        #Options:
        #N_trials :     Number of trials

        #Note: The Q-values are not reset. Therefore, running this routine
        #several times will continue the learning process. If you want to run
        #a completely new simulation, call reset() before running it.
        
        
        for self.trial in range(self.N_trials):            
            self.Trial = self.trial
            self.Run = 0
            self.e = numpy.zeros((self.Nn,self.Nn,4))
            self.epsilon = np.exp(-self.Trial/1.0*self.tau)
            # run a trial and store the time it takes to the target
            latency = self._run_trial()
            if(self._reward() == 1): self.latency_list.append(latency)
            else: self.latency_list.append(3*self.Nn*self.Nn)
            if(self.video == 3): 
                if(self.trial%int(self.N_trials/25)==0 or self.trial==self.N_trials-1):    
                    self.sarsaad.latency(self.latency_list,self.N_trials,self.Nn)
                    if(self.trial==self.N_trials-1): time.sleep(15)
                    else: time.sleep(0.5)

        return array(self.latency_list)
    
    
    def _run_trial(self,visualize=False):
        #print "_run_trial"
        
        #Run a single trial on the gridworld until the agent reaches the reward position.
        #Return the time it takes to get there.

        #Options:
        #visual: If 'visualize' is 'True', show the time course of the trial graphically
        
        # choose the initial position and make sure that its not in the wall
        while True:
            self.x_position = numpy.random.randint(self.Nn)
            self.y_position = numpy.random.randint(self.Nn)
            
            self.x_start = self.x_position
            self.y_start = self.y_position
            
            if not self._is_wall(self.x_position,self.y_position):
                break
        
        
        #print "Starting trial at position ({0},{1}), reward at ({2},{3})".format(self.x_position,self.y_position,self.reward_position[0],self.reward_position[1])
        #if self.obstacle:
        #      print "Obstacle is in position (?,?)"

        # initialize the latency (time to reach the target) for this trial
        latency = 0.

        # start the visualization, if asked for
        if visualize:
            self._init_visualization()    
            
        # run the trial
        #print self.Trial
        self._choose_action()
        arrived = False
        while (not arrived) and (latency < 3*self.Nn*self.Nn): #(not self._arrived()) and (not arrived):
            self._update_state()
            self._choose_action()    
            arrived = self._update_Q()
            self.Run += 1
            if visualize:
                self._visualize_current_state()
        
            latency = latency + 1

        if visualize:
            self._close_visualization()
        return latency
    
    ###############################################################################################
    # 
    #
    ###############################################################################################

    def _update_Q(self):
        #print "_update_Q"
        """
        Update the current estimate of the Q-values according to SARSA.
        """
        # update the eligibility trace
        self.e = self.lambda_eligibility * self.e
        self.e[self.x_position_old, self.y_position_old,self.action_old] += 1.
        
        # update the Q-values
        if self.action_old != None:
            self.Q +=     \
                self.eta * self.e *\
                (self._reward()  \
                - ( self.Q[self.x_position_old,self.y_position_old,self.action_old] \
                - self.gamma * self.Q[self.x_position, self.y_position, self.action] )  )
        
        if(self._reward() != 0.0): return True
        else: return False

    def _choose_action(self):  
        #print "_choose_action"
        """
        Choose the next action based on the current estimate of the Q-values.
        The parameter epsilon determines, how often agent chooses the action 
        with the highest Q-value (probability 1-epsilon). In the rest of the cases
        a random action is chosen.
        """
        self.action_old = self.action
        if numpy.random.rand() < self.epsilon:
            self.action = numpy.random.randint(4)
        else:
            self.action = argmax(self.Q[self.x_position,self.y_position,:])    
    
    def _arrived(self):
        #print "_arrived"
        """
        Check if the agent has arrived.
        """
        return ((self.x_position == self.reward_position[0] and \
				self.y_position == self.reward_position[1])) or \
				(self.Run > 3*self.Nn*self.Nn)# or \
				#(self.Reward[self.x_position, self.y_position,self.action] != 0.0)

    def _reward(self):
        #print "_reward"
        """
        Evaluates how much reward should be administered when performing the 
        chosen action at the current location
        """
        return self.Reward[self.x_position_old, self.y_position_old,self.action_old]

    def _update_state(self):
        #print "_update_state"
        """
        Update the state according to the old state and the current action.    
        """
        # remember the old position of the agent
        self.x_position_old = self.x_position
        self.y_position_old = self.y_position
        
        # update the agents position according to the action
        #  move right
        if self.action == 0:
            self.x_position += 1
        # move left
        elif self.action == 1:
            self.x_position -= 1
        # move up
        elif self.action == 2:
            self.y_position += 1
        # move down
        elif self.action == 3:
            self.y_position -= 1
        else:
            print "There must be a bug. This is not a valid action!"
                        
        # check if the agent has bumped into a wall.
        if self._is_wall():
            self.x_position = self.x_position_old
            self.y_position = self.y_position_old
            self._wall_touch = True
            #print "#### wally ####"
        else:
            self._wall_touch = False
        
        #if(self.video == 1): self.visualization1()
        #if(self.video == 2): self.visualization2()
        #from SARSA_additional import SARSA_additional
        #sarsaad = SARSA_additional()
        
        if(0 < self.video < 3): 
			simdata = [self.Nn, self.Trial, self.Run]
			actdata = [self.x_position, self.y_position, self.x_position_old, self.y_position_old]
			Rdata = self.reward_position
			Sdata = [self.x_start, self.y_start]
			Qdata = self.Q[self.x_position][self.y_position][:]
			self.sarsaad.visualization(self.video, simdata, actdata, Rdata, Sdata, Qdata)
			if(self._wall_touch): time.sleep(3)

        

    def _is_wall(self,x_position=None,y_position=None):    
        #print "_is_wall"
        """
        This function returns, if the given position is within an obstacle
        If you want to put the obstacle somewhere else, this is what you have 
        to modify. The default is a wall that starts in the middle of the room
        and ends at the right wall.

        If no position is given, the current position of the agent is evaluated.
        """
        if x_position == None or y_position == None:
            x_position = self.x_position
            y_position = self.y_position
        
        # check of the agent is trying to leave the gridworld
        if x_position < 0 or x_position >= self.Nn or y_position < 0 or y_position >= self.Nn:
            return True
        """
        # check if the agent has bumped into an obstacle in the room
        if self.obstacle:
            if y_position == self.Nn/2 and x_position>self.Nn/2:
                return True
        """
        # if action is possible
        if(max(self.Reward[self.x_position,self.y_position,:]) < 0.0):
            return True
        
        # if none of the above is the case, this position is not a wall
        return False
