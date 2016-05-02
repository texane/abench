#!/usr/bin/env python


import numpy
import math
import re


#
# acquisition meta information.
# meta information consist of non sample but useful data

class Meta:
    def __init__(self):
        self.nchan = 1
        self.fsampl = None
        self.vref = [ None, None ]
        return

    def __str__(self):
        s = ''
        s += 'nchan : ' + str(self.nchan) + '\n'
        s += 'fsampl: ' + str(self.fsampl) + '\n'
        s += 'vref  : ' + str(self.vref) + '\n'
        return s


#
# file reader

class FileReader:
    def __init__(self):
        self._meta = Meta()
        self._file = None
        self._data = None
        self._err = None
        return

    def open(self, path):
        if self._file == None:
            try: self._file = open(path, 'r')
            except: return False
        return True

    def get_meta(self):
        return self._meta

    def get_err(self):
        return self._err


class ADCProFileReader(FileReader):
    _is_init = False

    @staticmethod
    def init_class():
        if ADCProFileReader._is_init == True: return

        # create rexps

        float_re = '([-+]?\d*\.?\d*)'
        ADCProFileReader.data_re = re.compile(
            '^\s*' + float_re + '$'
            )
        ADCProFileReader.fsampl_re = re.compile(
            '^Sampling Frequency\s*' + float_re + '$'
            )
        ADCProFileReader.nchan_re = re.compile(
            '^Number of Channels\s*' + float_re + '$'
            )
        ADCProFileReader.vmin_re = re.compile(
            '^Min Voltage\s*' + float_re + '$'
            )
        ADCProFileReader.vmax_re = re.compile(
            '^Max Voltage\s*' + float_re + '$'
            )
        ADCProFileReader.all_re = (
            ADCProFileReader.data_re,
            ADCProFileReader.fsampl_re,
            ADCProFileReader.nchan_re,
            ADCProFileReader.vmin_re,
            ADCProFileReader.vmax_re
            )

        return

    def __init__(self):
        FileReader.__init__(self)
        ADCProFileReader.init_class()
        return

    def match_next(self, l):
        for r in ADCProFileReader.all_re:
            m = r.search(l)
            if m == None or m.groups == 1: continue
            return float(m.group(1))

    def read(self, path = None):
        # already done

        if self._data != None: return self._data
        if path != None and self.open(path) == False: return None

        # parse file

        data = []

        while True:
            line = self._file.readline()
            if len(line) == 0: break
            line = line.strip()

            for r in ADCProFileReader.all_re:
                m = r.search(line)
                if m == None or m.groups == 1: continue
                # one found
                x = float(m.group(1))
                if r == ADCProFileReader.data_re: data.append(x)
                elif r == ADCProFileReader.fsampl_re: self._meta.fsampl = x
                elif r == ADCProFileReader.nchan_re: self._meta.nchan = x
                elif r == ADCProFileReader.vmin_re: self._meta.vref[0] = x
                elif r == ADCProFileReader.vmax_re: self._meta.vref[1] = x
                break

        # create data array

        self._data = numpy.array(data)
        return self._data


#
# analysis

class Analysis:
    def __init__(self):
        return


class NoiseAnalysis(Analysis):
    # DC noise analysis

    def __init__(self):
        self._noisefree_res = 0
        return

    def run(self, x):
        diff = x.max() - x.min()
        self._noisefree_res = 24 - math.ceil(math.log(diff, 2))
        return self._noisefree_res


#
# main


def main():
    reader = ADCProFileReader()
    samples = reader.read('../data/ads1259/0000.txt')
    print(str(NoiseAnalysis().run(samples)))
    return

main()
