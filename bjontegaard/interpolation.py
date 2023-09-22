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


import scipy.interpolate
import numpy as np


def interpolate(x, y, method: str):
    # makes sure that x and y coordinates are in increasing order
    if x[-1] < x[0]:
        assert (y[-1] < y[0])
        x = np.flipud(x)
        y = np.flipud(y)

    if method == 'akima':
        return interpolate_akima(x, y)
    elif method == 'pchip':
        return interpolate_pchip(x, y)
    elif method == 'cubic':
        return interpolate_cubic(x, y)
    else:
        raise ValueError("Invalid interpolation method '{}'. Only 'akima', 'pchip' and 'cubic' are allowed"
                         .format(method))


def interpolate_akima(x, y):
    if len(x) > 2:
        return scipy.interpolate.Akima1DInterpolator(x, y)
    else:
        return scipy.interpolate.make_interp_spline(x, y, k=1)


def interpolate_pchip(x, y):
    return scipy.interpolate.PchipInterpolator(x, y)


def interpolate_cubic(x, y):
    class CubicInterpolator:
        def __init__(self, _x, _y):
            self._coefficients = np.polyfit(_x, _y, 3)
            self._interpolator = np.poly1d(self._coefficients)
            self._integrator = np.polyint(self._coefficients)

        def __call__(self, _x):
            return self._interpolator(_x)

        def integrate(self, lower_bound, higher_bound):
            return np.polyval(self._integrator, higher_bound) - np.polyval(self._integrator, lower_bound)

    return CubicInterpolator(x, y)
