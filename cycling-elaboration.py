from cycling import Cycling

import tools as tls

import matplotlib.pyplot as plt
import numpy as np

import datetime

def compare_zones(reference,other,zone):

    for k,v in zone.items():

        print(k + "-> reference ride:",reference.time_in_zone(v))
        print(k + "->      this ride:",other.time_in_zone(v))

def ispra_laveno_analysis():

    reference_ride = Cycling()
    reference_ride.read_data('bike/ispra-laveno/2019-07-23-19-17-39.fit')

    this_ride = Cycling()
    this_ride.read_data('bike/ispra-laveno/2019-07-30-18-44-19.fit')

    zone = {"max":(165,180),
    "high_threshold":(160,165),
    "low_threshold":(155,160),
    "aerobic":(145,155)}

    compare_zones(reference_ride,this_ride,zone)

def locate_sprint(speed,duration):
    test = np.arange(0,duration)
    conv = np.convolve(speed,test)
    plt.plot(conv)
    plt.show()

def get_sprints(filename):

    ride = Cycling()
    ride.read_data(filename)

    ride.esitmate_power(90)

    return ride.get_sprint_data(30,10)


def sprint_analysis():

    ispra = get_sprints('bike/10xstill-start-sprint/2019-08-06-18-19-19.fit')

    ferrara = get_sprints("bike/10xstill-start-sprint/2019-05-23-19-10-47.fit")

    fig, ax = plt.subplots(2,5,figsize=(20,10))

    for i in range(2):
        for j in range(5):
            k = 2*i+j

            pisp = tls.non_negative(ispra[k].data["power"])
            pfe = tls.non_negative(ferrara[k].data["power"])

            eisp =  ispra[k].eavaluate_energy()
            efe =  ferrara[k].eavaluate_energy()

            lisp = 'august, energy = '+str(int(eisp))
            lfe = 'may, energy = '+str(int(efe))

            li = ax[i,j].plot(ispra[k].data["timestamp"],pisp,label=lisp)
            lf = ax[i,j].plot(ferrara[k].data["timestamp"],pfe,label=lfe)
            ax[i,j].legend(loc='lower center',bbox_to_anchor=(.5,-.1))

    fig.savefig("sprint-comparison.pdf", bbox_inches='tight')


    #fig, ax = plt.subplots(5,2)

    # for i in range(10):
    #     ax[i].plot(ispra[i].data["timestamp"],ispra[i].data["power"],'-')
    #     ax[i].plot(ferrara[i].data["timestamp"],ferrara[i].data["power"],'--')

    #plt.legend([li,lf], ['august-6','may-23'], loc='upper right', bbox_to_anchor=(0.5, -0.05))

    plt.show()


    #color = ['r','g','b']

    #for isp, fe in zip(ispra[:3], ferrara[:3]):
    #    plt.plot(isp.data["timestamp"],isp.data["power"],'-')
    #    plt.plot(fe.data["timestamp"],fe.data["power"],'--')

    plt.show()


if __name__ == "__main__":

    sprint_analysis()
