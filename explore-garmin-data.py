import os
from fitparse import FitFile
import numpy as np
import matplotlib.pyplot as plt

from cycling import Cycling

av_00 = Cycling()
av_00.read_data('7C9A5608.FIT')

av_01 = Cycling()
av_01.read_data('7CGE0257.FIT')

first_climb = Cycling()
av_00.output_interval(178,2363,first_climb,True)

second_climb = Cycling()
av_00.output_interval(4572,6620,second_climb,True)

third_climb = Cycling()
av_01.output_interval(200,2178,third_climb,True)


speed = third_climb.approximate_derivative("timestamp",
                                           "distance",5)

slope = third_climb.approximate_derivative("distance",
                                           "altitude",
                                           5)



plt.plot(third_climb.data["timestamp"],
         speed)
plt.plot(third_climb.data["timestamp"],
         slope*100)
plt.show()
