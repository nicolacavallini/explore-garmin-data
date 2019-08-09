import os
from fitparse import FitFile
import numpy as np
import tools as tls
import datetime

class Training(object):
    def __init__(self,smoothing_sample=5):
        self.data = {}
        self.data_length = 0
        self.i = 0
        self.smoothing_sample = smoothing_sample

    def read_data(self, filename):
        fitfile_path = os.path.join('data/', filename)
        print(fitfile_path)
        fitfile = FitFile(fitfile_path)
        fitfile.parse()

        records = list(fitfile.get_messages(name='record'))

        r0 = records[0]
        for field in r0:
            self.data[field.name] = []
            print("field: ", field.name, "units: ", field.units)
            if field.name == 'timestamp':
                t0 = field.value

        for r in records[1:]:
            for field in r:
                if field.name == 'timestamp':
                    t = field.value-t0
                    self.data['timestamp'].append(t.total_seconds())


        for r in records[1:]:
            for field in r:
                if field.name != 'timestamp':
                    if field.name in self.data:
                        self.data[field.name].append(field.value)
                    else:
                        self.data[field.name] = []
                        self.data[field.name].append(field.value)

        for k in self.data:
            v = np.array(self.data[k])
            print(k+" shape:",v.shape)
            self.data[k] = v

        self.data["timedelta"] = np.array([0])

        self.data["timedelta"] = np.hstack((self.data["timedelta"],np.diff(self.data["timestamp"])))

        self.data_length = len(self.data["timestamp"])

    def output_interval(self,start_record, end_record,interval,reset_time=False):
        ids = np.where((self.data["timestamp"] > start_record) & (self.data["timestamp"] < end_record))

        for k in self.data:
            interval.data[k] = self.data[k][ids]

        if reset_time:
            interval.data["timestamp"] = interval.data["timestamp"] - interval.data["timestamp"][0]

        interval.data_length = len(interval.data["timestamp"])
        interval.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.data_length:
            i = self.i
            if i < self.smoothing_sample:
                self.stencil_ids = np.arange(i,i+self.smoothing_sample)
            elif i > len(self.data["timestamp"])-self.smoothing_sample:
                self.stencil_ids = np.arange(i-self.smoothing_sample+1,i+1)
            else:
                self.stencil_ids  = np.arange(int(i-np.floor(self.smoothing_sample/2)),
                                              int(i+np.ceil(self.smoothing_sample/2)))
            self.i += 1
            return self
        else:
            self.i = 0
            raise StopIteration()

    def seconds_in_zone(self,zone):

        time = self.data["timedelta"]
        hr= self.data["heart_rate"]

        offset = len(time)-len(hr)

        time = time[offset:]

        assert len(time)==len(hr), "time and hr must have the same dimension"

        time_in_zone = 0

        for t, h in zip(time,hr):
            if (zone[0] < h and h < zone[1]):
                time_in_zone+=t

        return time_in_zone

    def time_in_zone(self,zone):
        return str(datetime.timedelta(seconds=self.seconds_in_zone(zone)))


    def construct_stemcil(self):
        for i in range(len(self.data["timestamp"])):
            if i < 2:
                ids = np.arange(i,3+i)
            elif i > len(self.data["timestamp"])-3:
                ids = np.arange(i-2,i+1)
            else:
                ids  = np.arange(i-3,i+2)
            print(ids)

    def interpolate_and_derive_data(self,coord_x, coord_y):
        f = []
        for s in self:
            x = self.data[coord_x][self.stencil_ids]
            y = self.data[coord_y][self.stencil_ids]
            sample = .5
            w = np.amax(x)-np.amin(x)
            der = tls.interpolate_and_get_derivative(x,y)(sample)/w
            f.append(der)
        return np.array(f)
