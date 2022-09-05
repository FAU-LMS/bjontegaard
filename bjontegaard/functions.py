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


from typing import Union, List, Tuple, Callable
import numpy as np
from . import bd_akima
from . import bd_cubic
from . import bd_piecewise_cubic


_ValueArray = Union[List[Union[int, float]], np.ndarray]
_Interpolator = Callable[[np.ndarray], np.ndarray]


def _check_points(n_rate_anchor, n_dist_anchor, n_rate_test, n_dist_test, require_matching_points):
    if n_rate_anchor != n_dist_anchor:
        raise ValueError("Number of rate and distortion points for anchor does not match.")
    if n_rate_test != n_dist_test:
        raise ValueError("Number of rate and distortion points for test does not match.")
    if require_matching_points and n_rate_anchor != n_rate_test:
        raise ValueError("Number of rate-distortion points for anchor and test does not match but "
                         "`require_matching_points == True`")


def bd_rate(rate_anchor: _ValueArray,
            dist_anchor: _ValueArray,
            rate_test: _ValueArray,
            dist_test: _ValueArray,
            method: str = 'pchip',
            require_matching_points=True,
            interpolators=False) -> Union[float, Tuple[float, _Interpolator, _Interpolator]]:
    """
    Calculate the Bjontegaard-Delta Rate using the specified interpolation method.

    :param rate_anchor: rates of reference codec
    :param dist_anchor: distortion metrics of reference codec
    :param rate_test: rates of investigated codec
    :param dist_test: distortion metrics of investigated codec
    :param method: interpolation method to use for Bjontegaard-Delta calculation ('akima', 'pchip' (default), 'cubic')
    :param require_matching_points: whether to require an equal number of rate-distortion points for anchor and test.
    (default: True)
    :param interpolators: whether to include the interpolation callables in the output (default: False)
    :returns: Bjontegaard-Delta Rate
    :returns: Only returned if `interpolators == True`. Interpolation callables for investigated and reference codec.
    :raises ValueError: if number of points for rate and distortion metric do not match
    :raises ValueError: if `require_matching_points == True` and number of rate-distortion points for anchor and test
    do not match
    :raises ValueError: if interpolation method is not valid
    """
    rate_anchor = np.asarray(rate_anchor)
    dist_anchor = np.asarray(dist_anchor)
    rate_test = np.asarray(rate_test)
    dist_test = np.asarray(dist_test)
    _check_points(len(rate_anchor), len(dist_anchor), len(rate_test), len(dist_test), require_matching_points)
    if method == 'akima':
        return bd_akima.bd_rate(rate_anchor, dist_anchor, rate_test, dist_test, interpolators)
    elif method == 'pchip':
        return bd_piecewise_cubic.bd_rate(rate_anchor, dist_anchor, rate_test, dist_test, interpolators)
    elif method == 'cubic':
        return bd_cubic.bd_rate(rate_anchor, dist_anchor, rate_test, dist_test, interpolators)
    else:
        raise ValueError("Invalid interpolation method '{}'. Only 'akima', 'pchip' and 'cubic' are allowed"
                         .format(method))


def bd_psnr(rate_anchor: _ValueArray,
            dist_anchor: _ValueArray,
            rate_test: _ValueArray,
            dist_test: _ValueArray,
            method: str = 'pchip',
            require_matching_points=True,
            interpolators=False) -> Union[float, Tuple[float, _Interpolator, _Interpolator]]:
    """
    Calculate the Bjontegaard-Delta PSNR using the specified interpolation method.

    :param rate_anchor: rates of reference codec
    :param dist_anchor: distortion metrics of reference codec
    :param rate_test: rates of investigated codec
    :param dist_test: distortion metrics of investigated codec
    :param method: interpolation method to use for Bjontegaard-Delta calculation ('akima', 'pchip' (default), 'cubic')
    :param require_matching_points: whether to require an equal number of rate-distortion points for anchor and test.
    (default: True)
    :param interpolators: whether to include the interpolation callables in the output (default: False)
    :returns: Bjontegaard-Delta PSNR
    :returns: Only returned if `interpolators == True`. Interpolation callables for investigated and reference codec.
    :raises ValueError: if number of points for rate and distortion metric do not match
    :raises ValueError: if `require_matching_points == True` and number of rate-distortion points for anchor and test
    do not match
    :raises ValueError: if interpolation method is not valid
    """
    rate_anchor = np.asarray(rate_anchor)
    dist_anchor = np.asarray(dist_anchor)
    rate_test = np.asarray(rate_test)
    dist_test = np.asarray(dist_test)
    _check_points(len(rate_anchor), len(dist_anchor), len(rate_test), len(dist_test), require_matching_points)
    if method == 'akima':
        return bd_akima.bd_PSNR(rate_anchor, dist_anchor, rate_test, dist_test, interpolators)
    elif method == 'pchip':
        return bd_piecewise_cubic.bd_PSNR(rate_anchor, dist_anchor, rate_test, dist_test, interpolators)
    elif method == 'cubic':
        return bd_cubic.bd_PSNR(rate_anchor, dist_anchor, rate_test, dist_test, interpolators)
    else:
        raise ValueError("Invalid interpolation method '{}'. Only 'akima', 'pchip' and 'cubic' are allowed"
                         .format(method))
