@nrp.MapRobotSubscriber('scan', Topic('/p3dx/laser/scan', sensor_msgs.msg.LaserScan))
@nrp.Robot2Neuron()
def p3dx_laser_scan_3(t, scan):
    # Auto generated TF for p3dx_laser_scan
    if t % 2 < 0.02:
        clientLogger.info('TF p3dx_laser_scan:', t)