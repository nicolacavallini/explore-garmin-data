from running import Running

import matplotlib.pyplot as plt
import numpy as np

import datetime


if __name__ == "__main__":

    run = Running()
    run.read_data('run/2019-07-31-18-09-14.fit')

    zone = {"max":(170,180),
    "high_threshold":(160,170),
    "low_threshold":(150,160),
    "aerobic":(140,150)}

    for k,v in zone.items():
        print(k + "-> run:",run.time_in_zone(v))
