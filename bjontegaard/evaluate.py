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

from . import functions as bd
import numpy as np
import matplotlib.pyplot as plt


def compare_methods(rate_anchor,
                    dist_anchor,
                    rate_test,
                    dist_test,
                    require_matching_points=True,
                    rate_label='rate',
                    distortion_label='PSNR',
                    figure_label=None,
                    filepath=None):
    """
    Plots a comparison of the internal behaviour of the different interpolation methods for BD calculations.

    :param rate_anchor: rates of reference codec
    :param dist_anchor: distortion metrics of reference codec
    :param rate_test: rates of investigated codec
    :param dist_test: distortion metrics of investigated codec
    :param require_matching_points: whether to require an equal number of rate-distortion points for anchor and test.
    (default: True)
    :param rate_label: Rate metric label (x-axis)
    :param distortion_label: Distortion metric label (y-axis)
    :param figure_label: Figure label (title)
    :param filepath: if filepath is given, final plot is stored to the given file
    :raises ValueError: if number of points for rate and distortion metric do not match
    :raises ValueError: if `require_matching_points == True` and number of rate-distortion points for anchor and test
    do not match
    :raises ValueError: if interpolation method is not valid
    """
    rate_anchor = np.asarray(rate_anchor)
    dist_anchor = np.asarray(dist_anchor)
    rate_test = np.asarray(rate_test)
    dist_test = np.asarray(dist_test)

    dists1 = np.linspace(dist_anchor.min(), dist_anchor.max(), num=10, endpoint=True)
    dists2 = np.linspace(dist_test.min(), dist_test.max(), num=10, endpoint=True)

    # Plot interpolation curves for each method
    methods = {
        'cubic': ('Cubic interpolation (non-piece-wise)', np.log),
        'pchip': ('Piece-wise cubic interpolation', np.log10),
        'akima': ('BD Calculation with Akima Interpolation', np.log10)
    }
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(figure_label)
    for ax, (method, (label, log)) in zip(axs.flat, methods.items()):
        bd_rate, interp1, interp2 = bd.bd_rate(rate_anchor, dist_anchor, rate_test, dist_test,
                                               method=method,
                                               require_matching_points=require_matching_points,
                                               interpolators=True)
        bd_psnr = bd.bd_psnr(rate_anchor, dist_anchor, rate_test, dist_test, method=method, require_matching_points=require_matching_points)

        # Plot rate1 and dist1
        rates1 = interp1(dists1)
        ax.plot(log(rate_anchor), dist_anchor, '-o', color='tab:blue', label='anchor')
        ax.plot(rates1, dists1, '--', color='tab:blue')

        # Plot rate2 and dist1
        rates2 = interp2(dists2)
        ax.plot(log(rate_test), dist_test, '-o', color='tab:orange', label='test')
        ax.plot(rates2, dists2, '--', color='tab:orange')

        # Set axis properties
        ax.set_title(label)
        ax.set_xlabel('{}({})'.format(log.__name__, rate_label))
        ax.set_ylabel(distortion_label)
        ax.grid()
        ax.legend()

        # Add bd metrics table
        cell_text = [
            ["{:.10f} %".format(bd_rate)],
            ["{:.10f} dB".format(bd_psnr)]
        ]
        ax.table(cellText=cell_text, rowLabels=["BD-Rate", "BD-PSNR"],
                 colWidths=[0.3, 0.1], loc="lower right", zorder=10)

    # Remove unused axes
    if len(axs.flat) > len(methods):
        for ax in axs.flat[len(methods):]:
            ax.axis('off')

    # Save if filepath is given
    if filepath is not None:
        fig.savefig(filepath, dpi=fig.dpi)

    plt.show()
