# -*- coding: utf-8 -*-
"""
This is a brain with 2 sensory neurons connected to 2 actor neurons.
This brain reproduce the 'Explorer' behavior of Braitenberg vehicle 3b.
There is one small difference : connections are excitatory,
the activity of actor neurons is subtracted to ongoing movement in the transfer function 'velocity_commands', thus reproducing the inhibitory effect.
"""
__author__ = 'Loic Jeanningros'
from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
import logging
logger = logging.getLogger(__name__)

def create_brain():
    # Brain simulation set-up
    sim.setup(timestep=0.1, min_delay=0.1, max_delay=20.0, threads=1, rng_seeds=[1234])
    
    ## NEURONS ##
    # Neuronal parameters
    NEURONPARAMS = {'cm': 0.025,
                    'v_rest': -60.5,
                    'tau_m': 10.,
                    'e_rev_E': 0.0,
                    'e_rev_I': -75.0,
                    'v_reset': -60.5,
                    'v_thresh': -60.0,
                    'tau_refrac': 10.0,
                    'tau_syn_E': 2.5,
                    'tau_syn_I': 2.5}
    # Build the neuronal model
    cell_class = sim.IF_cond_alpha(**NEURONPARAMS)
    # Define the neuronal population
    population = sim.Population(size=4, cellclass=cell_class)

    ## SYNAPSES ##
    # Build the weights matrix
    weights = np.zeros((2,2))
    weights[0,1] = 1.
    weights[1,0] = 1.
    weights *= 5e-5
    # Synaptic parameters
    SYNAPSE_PARAMS = {"weight": weights,
                      "delay": 1.0,
                      'U': 1.0,
                      'tau_rec': 1.0,
                      'tau_facil': 1.0}
    # Build synaptic model
    synapse_type = sim.TsodyksMarkramSynapse(**SYNAPSE_PARAMS)
    
    ## NETWORK ##
    # Connect neurons
    connector = sim.AllToAllConnector()
    sim.Projection(presynaptic_population=population[0:2],
                   postsynaptic_population=population[2:4],
                   connector=connector,
                   synapse_type=synapse_type,
                   receptor_type='excitatory')
    # Initialize the network
    sim.initialize(population, v=population.get('v_rest'))

    return population

circuit = create_brain()