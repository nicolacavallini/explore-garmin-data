from cycling import Cycling

import matplotlib.pyplot as plt
import numpy as np

import datetime

def compare_zones(reference,other,zone):

    for k,v in zone.items():

        print(k + "-> reference ride:",reference.time_in_zone(v))
        print(k + "->      this ride:",other.time_in_zone(v))

if __name__ == "__main__":

    reference_ride = Cycling()
    reference_ride.read_data('2019-07-23-19-17-39.fit')

    this_ride = Cycling()
    this_ride.read_data('2019-07-30-18-44-19.fit')

    zone = {"max":(165,180),
    "high_threshold":(160,165),
    "low_threshold":(155,160)}

    compare_zones(reference_ride,this_ride,zone)
