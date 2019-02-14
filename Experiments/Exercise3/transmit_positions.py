@nrp.MapRobotPublisher("tf_lattice", Topic('/tf/lattice', std_msgs.msg.Float64MultiArray))
@nrp.MapRobotPublisher("tf_pathway", Topic('/tf/pathway', std_msgs.msg.Float64MultiArray))
@nrp.Robot2Neuron()
def transmit_positions (t, tf_lattice, tf_pathway):
    from load_csv_positions import load_lattice, load_waypoints
    import math
    import numpy
    import csv
    
    # Load the SOM-lattice from a csv file 
    lattice_positions = load_lattice()
    Nn = lattice_positions.shape[0]
    # Load the waypoints from a csv file 
    waypoints = load_waypoints()
    Nw = waypoints.shape[0]
    
    #=============================================== 
    # Let's build a 3x3 matrix encoding our lattice:
    #================================================
    lattice = std_msgs.msg.Float64MultiArray()
    lattice.layout.dim.extend([std_msgs.msg.MultiArrayDimension()] * 3)
    lattice.layout.dim[0].label = "height"
    lattice.layout.dim[1].label = "width"
    lattice.layout.dim[2].label = "length"
    lattice.layout.dim[0].size = Nn
    lattice.layout.dim[1].size = Nn
    lattice.layout.dim[2].size = 2
    lattice.layout.dim[0].stride = Nn * Nn * 2
    lattice.layout.dim[1].stride = Nn * 2
    lattice.layout.dim[2].stride = 2
    lattice.layout.data_offset = 0
    lattice.data = [0] * Nn * Nn * 2
    # Set a few dimensions:
    dstride0 = lattice.layout.dim[0].stride
    dstride1 = lattice.layout.dim[1].stride
    dstride2 = lattice.layout.dim[2].stride
    offset = lattice.layout.data_offset

    for i in range(Nn):
        for j in range(Nn):
            for l in range(2):
                num = lattice_positions[i,j,l]
                lattice.data[offset + dstride1 * i + dstride2 * j + l] = num

    #===============================================  
    # Let's build a 2x2 matrix encoding our pathway:
    #===============================================
    pathway = std_msgs.msg.Float64MultiArray()
    pathway.layout.dim.extend([std_msgs.msg.MultiArrayDimension()] * 2)
    pathway.layout.dim[0].label = "x"
    pathway.layout.dim[1].label = "y"
    pathway.layout.dim[0].size = Nw
    pathway.layout.dim[1].size = 2
    pathway.layout.dim[0].stride = Nw * 2
    pathway.layout.dim[1].stride = 2
    pathway.layout.data_offset = 0
    pathway.data = [0]* Nw * 2
    # Set a few dimensions:
    dstride3 = pathway.layout.dim[0].stride
    dstride4 = pathway.layout.dim[1].stride
    offset = lattice.layout.data_offset

    for i in range(Nw):
        x = waypoints[i, 0]
        y = waypoints[i, 1]
        pathway.data[offset + dstride4 * i + 0] = lattice_positions[x, y, 0]     
        pathway.data[offset + dstride4 * i + 1] = lattice_positions[x, y, 1]
                     
    if t < 3:
        tf_lattice.send_message(std_msgs.msg.Float64MultiArray(lattice.layout, lattice.data))
    if 3 < t < 6:
        tf_pathway.send_message(std_msgs.msg.Float64MultiArray(pathway.layout, pathway.data))
