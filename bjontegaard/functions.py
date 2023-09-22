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


from typing import Union, List, Tuple, Callable
import numpy as np
import matplotlib.pyplot as plt
from .bjontegaard_delta import bjontegaard_delta


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


def bd_linear(base_anchor: _ValueArray,
              metric_anchor: _ValueArray,
              base_test: _ValueArray,
              metric_test: _ValueArray,
              method: str,
              require_matching_points=True,
              interpolators=False,
              min_overlap=0.75) -> Union[float, Tuple[float, _Interpolator, _Interpolator]]:
    """
    Linear Bjontegaard-Delta calculating the average metric difference averaged over the overlap
    interval of the base variable of anchor and test using the specified interpolation method.

    'bd_linear' means that no log scaling (or any other scaling) is applied to the base or metric variables. The only
    difference to 'bd_rate' and 'bd_psnr' is the applied log scaling to the rate variable.

    For Bjontegaard-Delta calculations, the given data points (base_anchor, metric_anchor), (base_test, metric_test)
    are interpreted as domain and codomain of a continuous function, i.e., metric_anchor = f_anchor(base_anchor),
    metric_test = f_test(base_test). The Bjontegaard-Delta value specifies the average improvement of the test metric
    over the anchor metric in the overlap interval of the base points of anchor and test. The functions f_anchor
    and f_test are approximated through interpolation using the provided data points (base_anchor, metric_anchor)
    and (base_test, metric_test) using the specified interpolation method.

    :param base_anchor: data points of base variable for anchor (independent variable)
    :param metric_anchor: data points of metric variable for anchor (dependent variable)
    :param base_test: data points of base variable for test (independent variable)
    :param metric_test: data points of metric variable for test (dependent variable)
    :param method: interpolation method to use for Bjontegaard-Delta calculation ('akima', 'pchip', 'cubic')
    :param require_matching_points: whether to require an equal number of rate-distortion points for anchor and test.
    (default: True)
    :param interpolators: whether to include the interpolation callables in the output (default: False)
    :param min_overlap: minimum relative overlap of anchor and test along base before raising a warning
    :returns: (Linear) Bjontegaard-Delta metric
    :returns: Only returned if `interpolators == True`. Interpolation callables for investigated and reference codec.
    :raises ValueError: if number of points for rate and distortion metric do not match
    :raises ValueError: if `require_matching_points == True` and number of rate-distortion points for anchor and test
    do not match
    :raises ValueError: if interpolation method is not valid
    """
    base_anchor = np.asarray(base_anchor)
    metric_anchor = np.asarray(metric_anchor)
    base_test = np.asarray(base_test)
    metric_test = np.asarray(metric_test)
    _check_points(len(base_anchor), len(metric_anchor), len(base_test), len(metric_test), require_matching_points)

    return bjontegaard_delta(base_anchor, metric_anchor, base_test, metric_test, method, interpolators, min_overlap)


def bd_rate(rate_anchor: _ValueArray,
            dist_anchor: _ValueArray,
            rate_test: _ValueArray,
            dist_test: _ValueArray,
            method: str,
            require_matching_points=True,
            interpolators=False,
            min_overlap=0.75) -> Union[float, Tuple[float, _Interpolator, _Interpolator]]:
    """
    Calculate the Bjontegaard-Delta Rate using the specified interpolation method.

    :param rate_anchor: rates of reference codec
    :param dist_anchor: distortion metrics of reference codec
    :param rate_test: rates of investigated codec
    :param dist_test: distortion metrics of investigated codec
    :param method: interpolation method to use for Bjontegaard-Delta calculation ('akima', 'pchip', 'cubic')
    :param require_matching_points: whether to require an equal number of rate-distortion points for anchor and test.
    (default: True)
    :param interpolators: whether to include the interpolation callables in the output (default: False)
    :param min_overlap: minimum relative overlap of anchor and test along distortion metric before raising a warning
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

    rate_anchor = np.log10(rate_anchor)
    rate_test = np.log10(rate_test)

    output = bd_linear(dist_anchor, rate_anchor,
                       dist_test, rate_test,
                       method,
                       require_matching_points,
                       interpolators,
                       min_overlap)

    def bdlograte_to_percent(bdlograte):
        return ((10 ** bdlograte) - 1) * 100

    if interpolators:
        output = bdlograte_to_percent(output[0]), output[1], output[2]
    else:
        output = bdlograte_to_percent(output)

    return output


def bd_psnr(rate_anchor: _ValueArray,
            dist_anchor: _ValueArray,
            rate_test: _ValueArray,
            dist_test: _ValueArray,
            method: str,
            require_matching_points=True,
            interpolators=False,
            min_overlap=0.75) -> Union[float, Tuple[float, _Interpolator, _Interpolator]]:
    """
    Calculate the Bjontegaard-Delta PSNR using the specified interpolation method.

    :param rate_anchor: rates of reference codec
    :param dist_anchor: distortion metrics of reference codec
    :param rate_test: rates of investigated codec
    :param dist_test: distortion metrics of investigated codec
    :param method: interpolation method to use for Bjontegaard-Delta calculation ('akima', 'pchip', 'cubic')
    :param require_matching_points: whether to require an equal number of rate-distortion points for anchor and test.
    (default: True)
    :param interpolators: whether to include the interpolation callables in the output (default: False)
    :param min_overlap: minimum relative overlap of anchor and test along rate before raising a warning
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

    rate_anchor = np.log10(rate_anchor)
    rate_test = np.log10(rate_test)

    return bd_linear(rate_anchor, dist_anchor,
                     rate_test, dist_test,
                     method,
                     require_matching_points,
                     interpolators,
                     min_overlap)


def plot_rcd(rate_anchor: _ValueArray,
             dist_anchor: _ValueArray,
             rate_test: _ValueArray,
             dist_test: _ValueArray,
             method: str,
             require_matching_points=True,
             samples=1000):
    """
    Shows the interpolated RD-curves and the RCD-plot (relative curve difference) using the specified
    interpolation method.

    :param rate_anchor: rates of reference codec
    :param dist_anchor: distortion metrics of reference codec
    :param rate_test: rates of investigated codec
    :param dist_test: distortion metrics of investigated codec
    :param method: interpolation method to use for Bjontegaard-Delta calculation ('akima', 'pchip', 'cubic')
    :param require_matching_points: whether to require an equal number of rate-distortion points for anchor and test.
    (default: True)
    :param samples: number of samples along distortion metric to use for plotting (default: 1000)
    :returns: None
    :raises ValueError: if number of points for rate and distortion metric do not match
    :raises ValueError: if `require_matching_points == True` and number of rate-distortion points for anchor and test
    do not match
    :raises ValueError: if interpolation method is not valid
    """
    rate_anchor = np.asarray(rate_anchor)
    dist_anchor = np.asarray(dist_anchor)
    rate_test = np.asarray(rate_test)
    dist_test = np.asarray(dist_test)
    bd_value, interp_anchor, interp_test = bd_rate(rate_anchor, dist_anchor,
                                                   rate_test, dist_test,
                                                   method, require_matching_points, interpolators=True)

    dist_anchor_min = np.min(dist_anchor)
    dist_anchor_max = np.max(dist_anchor)
    dist_test_min = np.min(dist_test)
    dist_test_max = np.max(dist_test)
    dist_union_min = np.min((dist_anchor_min, dist_test_min))
    dist_union_max = np.max((dist_anchor_max, dist_test_max))
    dist_intersection_min = np.max((dist_anchor_min, dist_test_min))
    dist_intersection_max = np.min((dist_anchor_max, dist_test_max))

    dists_union = np.linspace(dist_union_min, dist_union_max, num=samples, endpoint=True)
    mask_anchor = (dists_union >= dist_anchor_min) & (dists_union <= dist_anchor_max)
    mask_test = (dists_union >= dist_test_min) & (dists_union <= dist_test_max)
    mask_intersection = (dists_union >= dist_intersection_min) & (dists_union <= dist_intersection_max)

    rates_union_anchor = interp_anchor(dists_union)
    rates_union_test = interp_test(dists_union)

    curve_difference = rates_union_test[mask_intersection] - rates_union_anchor[mask_intersection]
    relative_curve_difference = 100 * (np.power(10, curve_difference) - 1)

    dist_anchor_intersection = dist_anchor[(dist_anchor >= dist_intersection_min) &
                                           (dist_anchor <= dist_intersection_max)]
    curve_difference_anchor = interp_test(dist_anchor_intersection) - interp_anchor(dist_anchor_intersection)
    relative_curve_difference_anchor = 100 * (np.power(10, curve_difference_anchor) - 1)

    dist_test_intersection = dist_test[(dist_test >= dist_intersection_min) & (dist_test <= dist_intersection_max)]
    curve_difference_test = interp_test(dist_test_intersection) - interp_anchor(dist_test_intersection)
    relative_curve_difference_test = 100 * (np.power(10, curve_difference_test) - 1)

    fig, axs = plt.subplots(1, 2, figsize=(7.5, 5))
    axs[0].plot(np.power(10, rates_union_anchor[mask_anchor]), dists_union[mask_anchor], color='tab:blue')
    axs[0].plot(np.power(10, rates_union_test[mask_test]), dists_union[mask_test], color='tab:orange')
    axs[0].scatter(rate_anchor, dist_anchor, marker='x', label='RD Anchor', color='tab:blue')
    axs[0].scatter(rate_test, dist_test, marker='o', facecolor='none', edgecolor='tab:orange', label='RD Test')
    axs[0].set_xscale('log')
    axs[0].grid(True, which="both")
    axs[0].set_ylim((dist_union_min, dist_union_max))
    axs[0].set_xlabel("Rate")
    axs[0].set_ylabel("PSNR")
    axs[0].legend()

    axs[1].plot(relative_curve_difference, dists_union[mask_intersection], color='tab:green', label='RCD')
    axs[1].axvline(bd_value, linestyle="--", color='tab:green', label='BD-Rate')
    axs[1].scatter(relative_curve_difference_anchor, dist_anchor_intersection,
                   color='tab:blue', marker='x', label="Points Anchor")
    axs[1].scatter(relative_curve_difference_test, dist_test_intersection,
                   facecolor='none', edgecolor='tab:orange', marker='o', label="Points Test")
    axs[1].grid(True, which="both")
    axs[1].set_ylim((dist_union_min, dist_union_max))
    axs[1].set_xlabel("Relative Rate Difference (%)")
    axs[1].set_ylabel("PSNR")
    axs[1].legend()
    plt.show()
