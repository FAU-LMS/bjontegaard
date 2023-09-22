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


import warnings
from .interpolation import interpolate


def bjontegaard_delta(base_anchor, metric_anchor, base_test, metric_test, method, interpolators):
    # Compute the overlap (integration) interval
    overlap_interval_min = max(base_anchor.min(), base_test.min())
    overlap_interval_max = min(base_anchor.max(), base_test.max())

    # If overlap_interval_min is bigger than overlap_interval_max, the curves of both sequences don't overlap.
    if overlap_interval_min > overlap_interval_max:
        warnings.warn("Curves do not overlap. BD cannot be calculated.")
        return float("nan")

    f_anchor = interpolate(base_anchor, metric_anchor, method)
    f_test = interpolate(base_test, metric_test, method)

    # Calculate the integrated value over the interval we care about
    integrated_anchor = f_anchor.integrate(overlap_interval_min, overlap_interval_max)
    integrated_test = f_test.integrate(overlap_interval_min, overlap_interval_max)

    # Calculate the average improvement
    avg = (integrated_test - integrated_anchor) / (overlap_interval_max - overlap_interval_min)

    if interpolators:
        return avg, f_anchor, f_test
    else:
        return avg
