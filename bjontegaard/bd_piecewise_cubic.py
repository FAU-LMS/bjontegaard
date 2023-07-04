# BSD 3-Clause License
#
# Copyright (c) 2022-2023, Friedrich-Alexander-Universität Erlangen-Nürnberg.
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


def bd(xA, yA, xB, yB, interpolators=False):
    interp1, interp2 = _make_interpolators(xA, yA, xB, yB)

    # Integration interval.
    x_min = max(xA.min(), xB.min())
    x_max = min(xA.max(), xB.max())

    # Calculate the integrated value over the interval we care about.
    int1 = interp1.integrate(x_min, x_max)
    int2 = interp2.integrate(x_min, x_max)

    # Calculate the average improvement.
    avg = (int2 - int1) / (x_max - x_min)

    output = avg
    if interpolators:
        output = (output, interp1, interp2)
    return output


def bd_rate(rateA, distA, rateB, distB, interpolators=False):
    """Computes the Bjøntegaard bitrate (%) based on the Piecewise Cubic Hermite Interpolating Polynomial"""
    rateA = np.asarray(rateA)
    distA = np.asarray(distA)
    rateB = np.asarray(rateB)
    distB = np.asarray(distB)

    rateA, distA, rateB, distB = _ensure_monotonic(rateA, distA, rateB, distB)

    rateA = np.log10(rateA)
    rateB = np.log10(rateB)

    output = bd(distA, rateA, distB, rateB, interpolators=interpolators)

    if interpolators:
        (output, interp1, interp2) = output
    # Convert to a percentage.
    output = ((10 ** output) - 1) * 100
    if interpolators:
        output = (output, interp1, interp2)

    return output


def bd_PSNR(rateA, distA, rateB, distB, interpolators=False):
    """Computes the average PSNR difference based on the Piecewise Cubic Hermite Interpolating Polynomial"""
    rateA = np.array(rateA)
    distA = np.array(distA)
    rateB = np.array(rateB)
    distB = np.array(distB)

    rateA, distA, rateB, distB = _ensure_monotonic(rateA, distA, rateB, distB)

    rateA = np.log10(rateA)
    rateB = np.log10(rateB)

    return bd(rateA, distA, rateB, distB, interpolators=interpolators)


def _make_interpolators(xA, yA, xB, yB):
    # Compute Piecewise Cubic Hermite Interpolating Polynomial
    interp1 = scipy.interpolate.PchipInterpolator(xA, yA)
    interp2 = scipy.interpolate.PchipInterpolator(xB, yB)
    return interp1, interp2


def _ensure_monotonic(xA, yA, xB, yB):
    # makes sure that x and y coordinates are in increasing order
    if xA[-1] < xA[0]:
        assert yA[-1] < yA[0]
        xA = np.flipud(xA)
        yA = np.flipud(yA)

    if xB[-1] < xB[0]:
        assert yB[-1] < yB[0]
        xB = np.flipud(xB)
        yB = np.flipud(yB)

    return xA, yA, xB, yB
