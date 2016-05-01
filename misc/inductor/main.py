#!/usr/bin/env python

# http://www.itacanet.org/basic-electrical-engineering/part-6-electromagnetic-induction/
#
# filling equation
# I(t) = V0 / R * (1 - exp(-t * R / L))
# I(t) = I0 * (1 - exp(-t * R / L))
#
# decay equation
# I(t) = V0 / R * exp(-t * R / L)
# I(t) = I0 * exp(-t * R / L)


import array
import math


class DCCT:
    # top class: SensorInterface

    def __init__(self, tau, ratio, rmeas, i0):
        self._tau = tau
        self._ratio = ratio
        self._rmeas = rmeas
        self._i0 = i0
        return

    def gen_points(self, tmin = 0.0, tmax = 0.0, dt = 0.0):
        n = int(math.ceil((tmax - tmin) / dt))
        x = array.array('f', [0.0] * n)
        for k in range(0, n):
            t = tmin + float(k) * dt
            x[k] = self._i0 * math.exp(-t / self._tau)
            x[k] /= self._ratio
            x[k] *= self._rmeas
        return x


class ADS1259:
    # top class: ADCInterface

    def __init__(self, nbits, noise, vmin, vmax, voff, vdrift):
        self._vmin = vmin
        self._vmax = vmax
        self._voff = voff
        self._vdrift = vdrift
        return

    def gen_points(self, tsampl = 0.0, fsampl = 0.0, sensor = None):
        x = sensor.gen_points(tmax = tsampl, dt = 1.0 / fsampl)
        return


def main():
    dcct = DCCT(tau = 0.01, ratio = 1000.0, rmeas = 10.0, i0 = 90)
    x = dcct.gen_points(tmax = 0.1, dt = 0.00001)
    for xx in x: print(str(xx))
    return

main()
