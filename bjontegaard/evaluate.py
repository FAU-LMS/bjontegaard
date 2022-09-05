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


def compare_methods(rate1,
                    dist1,
                    rate2,
                    dist2,
                    rate_label='rate',
                    distortion_label='PSNR',
                    figure_label=None,
                    filepath=None):
    rate1 = np.asarray(rate1)
    dist1 = np.asarray(dist1)
    rate2 = np.asarray(rate2)
    dist2 = np.asarray(dist2)

    dists1 = np.linspace(dist1.min(), dist1.max(), num=10, endpoint=True)
    dists2 = np.linspace(dist2.min(), dist2.max(), num=10, endpoint=True)

    # Plot interpolation curves for each method
    methods = {
        'cubic': ('Cubic interpolation (non-piece-wise)', np.log),
        'pchip': ('Piece-wise cubic interpolation', np.log10),
        'akima': ('BD Calculation with Akima Interpolation', np.log10)
    }
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(figure_label)
    for ax, (method, (label, log)) in zip(axs.flat, methods.items()):
        bd_rate, interp1, interp2 = bd.bd_rate(rate1, dist1, rate2, dist2, method=method, interpolators=True)
        bd_psnr = bd.bd_psnr(rate1, dist1, rate2, dist2, method=method)

        # Plot rate1 and dist1
        rates1 = interp1(dists1)
        ax.plot(log(rate1), dist1, '-o', color='tab:blue', label='encoder1')
        ax.plot(rates1, dists1, '--', color='tab:blue')

        # Plot rate2 and dist1
        rates2 = interp2(dists2)
        ax.plot(log(rate2), dist2, '-o', color='tab:orange', label='encoder2')
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
