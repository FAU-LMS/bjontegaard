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


def bd_rate(rate1: _ValueArray,
            dist1: _ValueArray,
            rate2: _ValueArray,
            dist2: _ValueArray,
            method: str,
            interpolators=False) -> Union[float, Tuple[float, _Interpolator, _Interpolator]]:
    """
    Calculate the Bjontegaard-Delta Rate using the specified interpolation method.

    :param rate1: rates of reference codec
    :param dist1: distortion metrics of reference codec
    :param rate2: rates of investigated codec
    :param dist2: distortion metrics of investigated codec
    :param method: interpolation method to use for Bjontegaard-Delta calculation ('akima', 'pchip', 'cubic')
    :param interpolators: whether to include the interpolation callables in the output (default: False)
    :returns: Bjontegaard-Delta Rate
    :returns: Only returned if `interpolators == True`. Interpolation callables for investigated and reference codec.
    :raises ValueError: if interpolation method is not valid
    """
    rate1 = np.asarray(rate1)
    dist1 = np.asarray(dist1)
    rate2 = np.asarray(rate2)
    dist2 = np.asarray(dist2)
    if method == 'akima':
        return bd_akima.bd_rate(rate1, dist1, rate2, dist2, interpolators)
    elif method == 'pchip':
        return bd_piecewise_cubic.bd_rate(rate1, dist1, rate2, dist2, interpolators)
    elif method == 'cubic':
        return bd_cubic.bd_rate(rate1, dist1, rate2, dist2, interpolators)
    else:
        raise ValueError("Invalid interpolation method '{}'. Only 'akima', 'pchip' and 'cubic' are allowed"
                         .format(method))


def bd_psnr(rate1: _ValueArray,
            dist1: _ValueArray,
            rate2: _ValueArray,
            dist2: _ValueArray,
            method: str,
            interpolators=False) -> Union[float, Tuple[float, _Interpolator, _Interpolator]]:
    """
    Calculate the Bjontegaard-Delta PSNR using the specified interpolation method.

    :param rate1: rates of reference codec
    :param dist1: distortion metrics of reference codec
    :param rate2: rates of investigated codec
    :param dist2: distortion metrics of investigated codec
    :param method: interpolation method to use for Bjontegaard-Delta calculation ('akima', 'pchip', 'cubic')
    :param interpolators: whether to include the interpolation callables in the output (default: False)
    :returns: Bjontegaard-Delta PSNR
    :returns: Only returned if `interpolators == True`. Interpolation callables for investigated and reference codec.
    :raises ValueError: if interpolation method is not valid
    """
    rate1 = np.asarray(rate1)
    dist1 = np.asarray(dist1)
    rate2 = np.asarray(rate2)
    dist2 = np.asarray(dist2)
    if method == 'akima':
        return bd_akima.bd_PSNR(rate1, dist1, rate2, dist2, interpolators)
    elif method == 'pchip':
        return bd_piecewise_cubic.bd_PSNR(rate1, dist1, rate2, dist2, interpolators)
    elif method == 'cubic':
        return bd_cubic.bd_PSNR(rate1, dist1, rate2, dist2, interpolators)
    else:
        raise ValueError("Invalid interpolation method '{}'. Only 'akima', 'pchip' and 'cubic' are allowed"
                         .format(method))
