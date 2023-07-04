# Copyright 2014 Google.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Converts video encoding result data from text files to visualization
data source."""

__author__ = "jzern@google.com (James Zern),"
__author__ += "jimbankoski@google.com (Jim Bankoski)"
__author__ += "hta@gogle.com (Harald Alvestrand)"

# AH: source of this file: https://github.com/google/compare-codecs/blob/master/lib/visual_metrics.py
# Then slightly modified.


import math  # noqa: E402
import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402


def bd(xA, yA, xB, yB, interpolators=False):
    # Best cubic polyfit.
    poly1 = np.polyfit(xA, yA, 3)
    poly2 = np.polyfit(xB, yB, 3)

    # Integration interval.
    x_min = max(min(xA), min(xB))
    x_max = min(max(xA), max(xB))

    # TODO shouldn't this be an exception...?
    if x_min == x_max:
        return 0.0

    # Integrate poly1, and poly2.
    p_int1 = np.polyint(poly1)
    p_int2 = np.polyint(poly2)

    # Calculate the integrated value over the interval we care about.
    int1 = np.polyval(p_int1, x_max) - np.polyval(p_int1, x_min)
    int2 = np.polyval(p_int2, x_max) - np.polyval(p_int2, x_min)

    # Calculate the average improvement.
    avg_diff = (int2 - int1) / (x_max - x_min)

    output = avg_diff
    if interpolators:
        interp1 = np.poly1d(poly1)
        interp2 = np.poly1d(poly2)
        output = (output, interp1, interp2)
    return output


def bd_PSNR(rate1, dist1, rate2, dist2, interpolators=False):
    """
    BJONTEGAARD    Bjontegaard metric calculation
    Bjontegaard's metric allows to compute the average gain in bd_psnr between two
    bd_rate-rate2 curves [1].
    rate1,rate2 - RD points for curve 1
    rate1,distortion_reference - RD points for curve 2

    returns the calculated Bjontegaard metric 'dsnr'

    code adapted from code written by : (c) 2010 Giuseppe Valenzise
    http://www.mathworks.com/matlabcentral/fileexchange/27798-bjontegaard-metric/content/bjontegaard.m
    """
    # pylint: disable=too-many-locals
    # numpy seems to do tricks with its exports.
    # pylint: disable=no-member

    log_rate1 = np.log10(rate1)
    log_rate2 = np.log10(rate2)

    return bd(log_rate1, dist1, log_rate2, dist2, interpolators=interpolators)


def bd_rate(rate1, dist1, rate2, dist2, interpolators=False):
    """
    BJONTEGAARD    Bjontegaard metric calculation
    Bjontegaard's metric allows to compute the average % saving in bitrate
    between two bd_rate-rate2 curves [1].

    rate1,rate2 - RD points for curve 1
    rate1,distortion_reference - RD points for curve 2

    adapted from code from: (c) 2010 Giuseppe Valenzise

    """
    # numpy plays games with its exported functions.
    # pylint: disable=no-member
    # pylint: disable=too-many-locals

    log_rate1 = np.log10(rate1)
    log_rate2 = np.log10(rate2)

    # Calculate the average improvement.
    output = bd(dist1, log_rate1, dist2, log_rate2, interpolators=interpolators)

    if interpolators:
        output, interp1, interp2 = output

    # In really bad formed data the exponent can grow too large. clamp it.
    output = min(output, 200)

    # Convert to a percentage.
    output = (math.exp(output) - 1) * 100

    if interpolators:
        output = (output, interp1, interp2)

    return output
