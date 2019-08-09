from training import Training

import tools as tls

import numpy as np

import matplotlib.pyplot as plt

from scipy.signal import find_peaks

class Cycling(Training):
    def __init__(self):
        Training.__init__(self)

    def esitmate_power(self,mass):

        delta = np.diff(self.data["enhanced_altitude"])
        D = np.diff(self.data["distance"])
        Delta = np.sqrt(D**2.-delta**2.)

        theta = np.arctan(delta/Delta)

        self.data["force_gravity"] = 9.806*mass*np.sin(theta)

        delta_vel = np.diff(self.data["enhanced_speed"])
        delta_time = np.diff(self.data["timestamp"])

        offset = len(delta_time) - len(delta_vel)

        acceleration = delta_vel/delta_time[offset:]

        self.data["force_inertia"] = mass*acceleration
        self.data["energy"] = self.data["force_inertia"]*D[offset:]
        self.data["power"] = self.data["energy"]/delta_time[offset:]

    def locate_sprint(self,duration,num_of_sprints):

        test = np.arange(0,duration)

        speed = tls.normalize(self.data["enhanced_speed"])

        power = tls.normalize(self.data["power"])

        offset = len(speed) - len(power)

        speed = speed[offset:]

        t = self.data["timestamp"]

        offset = len(t) - len(power)

        t = t[offset:]

        func = lambda x : np.float64(x)/np.float64(duration)

        power_c = tls.forward_convolution(power,duration,func)

        power_c -= np.median(power_c)

        peack_conv, _ = find_peaks(power_c,  prominence=1, width=duration/6)
        peack_conv = np.partition(peack_conv, -num_of_sprints)[-num_of_sprints-1:-1]

        return t[peack_conv]

    def get_sprint_data(self,duration,num_of_sprints):

        start = self.locate_sprint(duration,num_of_sprints)

        sprints_list = []

        for s in start:

            sprint = Cycling()
            self.output_interval(s,s+duration*4,sprint,reset_time=True)

            sprints_list.append(sprint)

        return sprints_list

    def eavaluate_energy(self):

        p = tls.non_negative(self.data["power"])

        t = self.data["timestamp"]

        offset = len(t) - len(p)

        t = t[offset:]

        return np.trapz(p,t)
