# BSD 3-Clause License
#
# Copyright (c) 2022, Friedrich-Alexander-Universität Erlangen-Nürnberg.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
import scipy.interpolate
import warnings


def bd_rate(rateA, distA, rateB, distB, interpolators=False):

    # makes sure that x and y coordinates are in increasing order
    if rateA[-1] < rateA[0]:
        assert (distA[-1] < distA[0])
        rateA = np.flipud(rateA)
        distA = np.flipud(distA)

    if rateB[-1] < rateB[0]:
        assert (distB[-1] < distB[0])
        rateB = np.flipud(rateB)
        distB = np.flipud(distB)

    # computes interpolating polynomial via the Akima Interpolation method
    interp1 = scipy.interpolate.Akima1DInterpolator(distA, np.log10(rateA))
    interp2 = scipy.interpolate.Akima1DInterpolator(distB, np.log10(rateB))

    # compute the integration interval
    min_dist = max(distA.min(), distB.min())
    max_dist = min(distA.max(), distB.max())

    # if min_dist is bigger than max_, the curves of both sequences don't overlap - BD cannot be calculated!
    if min_dist > max_dist:
        warnings.warn("Curves do not overlap. BD cannot be calculated.")
        return float('nan')

    # calculate the integrated value over the interval we care about
    int1 = interp1.integrate(min_dist, max_dist)
    int2 = interp2.integrate(min_dist, max_dist)

    # calculate the average improvement
    avg = (int2 - int1) / (max_dist - min_dist)

    # convert to a percentage
    bdrate = ((10 ** avg) - 1) * 100

    output = bdrate
    if interpolators:
        output = (output, interp1, interp2)
    return output


def bd_PSNR(rateA, distA, rateB, distB, interpolators=False):

    # makes sure that x and y coordinates are in increasing order
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

    # computes interpolating polynomial via the Akima Interpolation method
    interp1 = scipy.interpolate.Akima1DInterpolator(rateA, distA)
    interp2 = scipy.interpolate.Akima1DInterpolator(rateB, distB)

    # compute the integration interval
    min_rate = max(rateA.min(), rateB.min())
    max_rate = min(rateA.max(), rateB.max())

    # if min_ is bigger than max_, the curves of both sequences don't overlap - BD cannot be calculated!
    if min_rate > max_rate:
        warnings.warn("Curves do not overlap. BD cannot be calculated.")
        return float('nan')

    # calculate the integrated value over the interval we care about
    int1 = interp1.integrate(min_rate, max_rate)
    int2 = interp2.integrate(min_rate, max_rate)

    # calculate the average improvement
    avg = (int2 - int1) / (max_rate - min_rate)

    output = avg
    if interpolators:
        output = (output, interp1, interp2)
    return output
