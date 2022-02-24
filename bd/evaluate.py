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

import sys
import numpy as np
from scipy import misc
from . import bd_akima
from . import bd_cubic
from . import bd_piecewise_cubic
import matplotlib.pyplot as plt

def compare(rate1, psnr1, rate2, psnr2, paramset=('rate','PSNR')):
	f = plt.figure(figsize=(12, 5))
	ax = f.add_subplot(1,1,1)
	bd_rate = bd_cubic.bd_rate(rate1, psnr1, rate2, psnr2, ax)    
	bd_PSNR = bd_cubic.bd_PSNR(rate1, psnr1, rate2, psnr2)
	
	print('BD ' + paramset[0] + ' Cubic:            ' + str("%.4f" %(bd_rate))+"%")
	print('BD ' + paramset[1] + ' Cubic:            ' + str("%.4f" %(bd_PSNR))+"dB")
	
	name = paramset[2] if len(paramset) >= 3 else 'none'
	#f.savefig(name + '.svg', dpi=f.dpi) 
	plt.show()
	
	f = plt.figure(figsize=(12, 5))
	ax = f.add_subplot(1,1,1)
	bd_rate = bd_piecewise_cubic.bd_rate(rate1, psnr1, rate2, psnr2, ax)
	bd_PSNR = bd_piecewise_cubic.bd_PSNR(rate1, psnr1, rate2, psnr2)
	
	print('BD ' + paramset[0] + ' Piecewise-cubic:  ' + str("%.4f" %(bd_rate))+"%")
	print('BD ' + paramset[1] + ' Piecewise-cubic:  ' + str("%.4f" %(bd_PSNR))+"dB")
	
	name = paramset[2] if len(paramset) >= 3 else 'none'
	#f.savefig(name + '.svg', dpi=f.dpi) 
	plt.show()

	f = plt.figure(figsize=(12, 5))
	ax = f.add_subplot(1,1,1)
	bd_rate = bd_akima.bd_rate(rate1, psnr1, rate2, psnr2, ax)
	bd_PSNR = bd_akima.bd_PSNR(rate1, psnr1, rate2, psnr2)
	
	print('BD ' + paramset[0] + ' Akima:            ' + str("%.4f" %(bd_rate))+"%")
	print('BD ' + paramset[1] + ' Akima:            ' + str("%.4f" %(bd_PSNR))+"dB")
	
	name = paramset[2] if len(paramset) >= 3 else 'none'
	#f.savefig(name + '.svg', dpi=f.dpi) 
	plt.show()
