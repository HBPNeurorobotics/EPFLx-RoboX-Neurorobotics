import hbp_nrp_cle.tf_framework as nrp
# This specifies that the neurons of the records population
# should be monitored. You can see them in the spike train widget
@nrp.NeuronMonitor(nrp.brain.circuit, nrp.spike_recorder)
def all_neurons_spike_monitor(t):
    # Uncomment to log into the 'log-console' visible in the simulation
    # clientLogger.info("Time: ", t)
    return True

