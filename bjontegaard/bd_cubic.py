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
import numpy  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402


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
    # map() is recommended against.
    # pylint: disable=bad-builtin

    # log_rate1 = map(math.log, rate1)
    # log_rate2 = map(math.log, rate1)
    log_rate1 = numpy.log(rate1)
    log_rate2 = numpy.log(rate2)

    # Best cubic poly fit for graph represented by log_ratex, psrn_x.
    poly1 = numpy.polyfit(log_rate1, dist1, 3)
    poly2 = numpy.polyfit(log_rate2, dist2, 3)

    # Integration interval.
    min_int = max([min(log_rate1), min(log_rate2)])
    max_int = min([max(log_rate1), max(log_rate2)])

    # Integrate poly1, and poly2.
    p_int1 = numpy.polyint(poly1)
    p_int2 = numpy.polyint(poly2)

    # Calculate the integrated value over the interval we care about.
    int1 = numpy.polyval(p_int1, max_int) - numpy.polyval(p_int1, min_int)
    int2 = numpy.polyval(p_int2, max_int) - numpy.polyval(p_int2, min_int)

    # Calculate the average improvement.
    if max_int != min_int:
        avg_diff = (int2 - int1) / (max_int - min_int)
    else:
        avg_diff = 0.0

    output = avg_diff
    if interpolators:
        interp1 = numpy.poly1d(poly1)
        interp2 = numpy.poly1d(poly2)
        output = (output, interp1, interp2)
    return output


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
    # pylint: disable=bad-builtin

    # log_rate1 = map(math.log, rate1)
    # log_rate2 = map(math.log, rate1)
    log_rate1 = numpy.log(rate1)
    log_rate2 = numpy.log(rate2)

    # Best cubic poly fit for graph represented by log_ratex, psrn_x.
    poly1 = numpy.polyfit(dist1, log_rate1, 3)
    poly2 = numpy.polyfit(dist2, log_rate2, 3)

    # Integration interval.
    min_int = max([min(dist1), min(dist2)])
    max_int = min([max(dist1), max(dist2)])

    # find integral
    p_int1 = numpy.polyint(poly1)
    p_int2 = numpy.polyint(poly2)

    # Calculate the integrated value over the interval we care about.
    int1 = numpy.polyval(p_int1, max_int) - numpy.polyval(p_int1, min_int)
    int2 = numpy.polyval(p_int2, max_int) - numpy.polyval(p_int2, min_int)

    # Calculate the average improvement.
    avg_exp_diff = (int2 - int1) / (max_int - min_int)

    # In really bad formed data the exponent can grow too large.
    # clamp it.
    if avg_exp_diff > 200:
        avg_exp_diff = 200

    # Convert to a percentage.
    avg_diff = (math.exp(avg_exp_diff) - 1) * 100

    output = avg_diff
    if interpolators:
        interp1 = numpy.poly1d(poly1)
        interp2 = numpy.poly1d(poly2)
        output = (output, interp1, interp2)
    return output
