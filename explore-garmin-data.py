import os
from fitparse import FitFile
import numpy as np
import matplotlib.pyplot as plt

import tools

av_00 = tools.Cycling()
av_00.read_data('7C9A5608.FIT')

av_01 = tools.Cycling()
av_01.read_data('7CGE0257.FIT')

first_climb = tools.Cycling()
av_00.output_interval(178,2363,first_climb,True)

second_climb = tools.Cycling()
av_00.output_interval(4572,6620,second_climb,True)

third_climb = tools.Cycling()
av_01.output_interval(200,2178,third_climb,True)

#third_climb.construct_stemcil()
third_climb.explore_data()

# plt.plot(first_climb.data["timestamp"],
#          first_climb.data["altitude"],'rx')
# plt.plot(second_climb.data["timestamp"],
#          second_climb.data["altitude"],'g-')
# plt.plot(third_climb.data["timestamp"],
#          third_climb.data["altitude"],'k-')
# plt.show()