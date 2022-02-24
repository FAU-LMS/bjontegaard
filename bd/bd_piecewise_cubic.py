#!/usr/bin/python
#
# Copyright (c) 2022 Friedrich-Alexander-Universität Erlangen-Nürnberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import numpy as np
import scipy.interpolate


def bd_rate(rateA, distA, rateB, distB, ax=None):

    rateA = np.array(rateA)
    distA = np.array(distA)
    rateB = np.array(rateB)
    distB = np.array(distB)

    # make sure that x and y coordinates are in increasing order
    if rateA[-1] < rateA[0]:
        assert (distA[-1] < distA[0])
        rateA = np.flipud(rateA)
        distA = np.flipud(distA)

    if rateB[-1] < rateB[0]:
        assert (distB[-1] < distB[0])
        rateB = np.flipud(rateB)
        distB = np.flipud(distB)

    # Compute Piecewise Cubic Hermite Interpolating Polynomial
    interp1 = scipy.interpolate.PchipInterpolator(distA, np.log10(rateA))
    interp2 = scipy.interpolate.PchipInterpolator(distB, np.log10(rateB))

    # Integration interval.
    minPSNR = max(distA.min(), distB.min())
    maxPSNR = min(distA.max(), distB.max())

    # Calculate the integrated value over the interval we care about.
    int1 = interp1.integrate(minPSNR, maxPSNR)
    int2 = interp2.integrate(minPSNR, maxPSNR)

    # Calculate the average improvement.
    avg = (int2 - int1) / (maxPSNR - minPSNR)

    # Convert to a percentage.
    bdrate = ((10 ** avg) - 1) * 100

    if ax:
        ax.set_title('Piece-wise cubic interpolation')
        # plot rateA and distA
        pA = ax.plot(np.log10(rateA), distA, '-o', label='encoder1')
        dists = np.linspace(distA.min(), distA.max(), num=10, endpoint=True)
        ax.plot(interp1(dists), dists, '--', color=pA[-1].get_color())
        # plot rateB and distB
        pB = ax.plot(np.log10(rateB), distB, '-o', label='encoder2')
        dists = np.linspace(distB.min(), distB.max(), num=10, endpoint=True)
        ax.plot(interp2(dists), dists, '--', color=pB[-1].get_color())
        ax.set_xlabel('log(rate)')
        ax.set_ylabel('PSNR')
        ax.grid()
        ax.legend()

    return bdrate


def bd_PSNR(rateA, distA, rateB, distB):

    rateA = np.array(rateA)
    distA = np.array(distA)
    rateB = np.array(rateB)
    distB = np.array(distB)

    # make sure that x and y coordinates are in increasing order
    if rateA[-1] < rateA[0]:
        assert (distA[-1] < distA[0])
        rateA = np.flipud(rateA)
        distA = np.flipud(distA)

    if rateB[-1] < rateB[0]:
        assert (distB[-1] < distB[0])
        rateB = np.flipud(rateB)
        distB = np.flipud(distB)

    rateA = np.log10(rateA)
    rateB = np.log10(rateB)

    # Compute Piecewise Cubic Hermite Interpolating Polynomial
    interp1 = scipy.interpolate.PchipInterpolator(rateA, distA)
    interp2 = scipy.interpolate.PchipInterpolator(rateB, distB)

    # Integration interval.
    minRate = max(rateA.min(), rateB.min())
    maxRate = min(rateA.max(), rateB.max())

    # Calculate the integrated value over the interval we care about.
    int1 = interp1.integrate(minRate, maxRate)
    int2 = interp2.integrate(minRate, maxRate)

    # Calculate the average improvement.
    avg = (int2 - int1) / (maxRate - minRate)

    return avg
