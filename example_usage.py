#!/usr/bin/python
# 
# Copyright (c) 2022 Friedrich-Alexander-Universität Erlangen-Nürnberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 

import numpy as np
from bd import bd_akima
from bd import bd_piecewise_cubic
from bd import evaluate

# Get test data to evaluate
rate1 = np.array([9487.76, 4593.60, 2486.44, 1358.24])
psnr1 = np.array([ 40.037,  38.615,  36.845,  34.851])
rate2 = np.array([9787.80, 4469.00, 2451.52, 1356.24])
psnr2 = np.array([ 40.121,  38.651,  36.970,  34.987])

# if paramset is not given, a default set of ('rate', 'PSNR', 'none') is assumed
# this set is needed for e.g. correct axis descriptors
# the last parameter in the set is used to give the saved figure an individual name
paramset = ('rate','PSNR') 

print('\nBD Demo using Cubic, Piecewise-cubic, and Akima interpolation:')
print('\nTest 1')
# the parameter 'save_plot' lets you determine whether the plot should be saved as an .svg or not
evaluate.compare(rate1, psnr1, rate2, psnr2, paramset, save_plot=False)


print('\n\nTest 2 for high bit rates')
rate1 = np.array([82472.76, 26875.24, 9487.76, 4593.6,])
psnr1 = np.array([43.825, 41.404, 40.037, 38.615,])
rate2 = np.array([99896.96, 33952.04, 9787.8, 4469.0,])
psnr2 = np.array([44.731, 41.875, 40.121, 38.651,])
paramset = ('rate','PSNR','testcase2') 

evaluate.compare(rate1, psnr1, rate2, psnr2, paramset, save_plot=False)
