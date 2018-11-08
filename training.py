import os
from fitparse import FitFile
import numpy as np
import tools as tls

class Training(object):
    def __init__(self,smoothing_sample=5):
        self.data = {}
        self.data_length = 0
        self.i = 0
        self.smoothing_sample = smoothing_sample

    def read_data(self, filename):
        fitfile_path = os.path.join('data', filename)
        fitfile = FitFile(fitfile_path)
        fitfile.parse()

        records = list(fitfile.get_messages(name='record'))

        r0 = records[0]
        for field in r0:
            self.data[field.name] = []
            print "field: ", field.name, "units: ", field.units
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
                    self.data[field.name].append(field.value)

        for k in self.data:
            v = np.array(self.data[k])
            self.data[k] = v

        self.data_length = len(self.data["timestamp"])

    def output_interval(self,start_record, end_record,interval,reset=False):
        ids = np.where((self.data["timestamp"] > start_record) & (self.data["timestamp"] < end_record))

        for k in self.data:
            interval.data[k] = self.data[k][ids]

        if reset:
            interval.data["timestamp"] = interval.data["timestamp"] - interval.data["timestamp"][0]

        interval.data_length = len(interval.data["timestamp"])
        interval.i = 0

    def __iter__(self):
        return self

    def next(self):
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



    def construct_stemcil(self):
        for i in range(len(self.data["timestamp"])):
            if i < 2:
                ids = np.arange(i,3+i)
            elif i > len(self.data["timestamp"])-3:
                ids = np.arange(i-2,i+1)
            else:
                ids  = np.arange(i-3,i+2)
            print ids

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
