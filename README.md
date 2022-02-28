# Bjøntegaard-Delta Interpolation
## Introduction
The Bjøntegaard-Delta (BD) metrics (delta bit rate and delta PSNR) described in [1]
are well known metrics to measure the
average differences between two rate-distortion (RD) curves. They are based on **cubic-spline interpolation (CSI)** (bd_cubic.py)
of the RD curves and [Matlab](https://www.mathworks.com/matlabcentral/fileexchange/41749-bjontegaard-metric-calculation-bd-psnr) 
as well as [Python](https://github.com/google/compare-codecs/blob/master/lib/visual_metrics.py) implementations are available on the internet.

However, this way of interpolation using a third-order polynomial leads to
problems for certain RD curve constellations and causes very misleading results.
This has also been experienced during the standardization of HEVC. Consequently, 
the so-called **piecewise cubic hermite interpolation (PCHIP)** (bd_piecewise_cubic.py) has been implemented in the JCT-VC Common Test Conditions (CTC) Excel 
sheet [[2]](http://phenix.int-evry.fr/jct/doc_end_user/documents/12_Geneva/wg11/JCTVC-L1100-v1.zip) for performance evaluation.
Nevertheless, only this Excel sheet, but no Python implementation is available yet. Thus, a Python implementation is provided here. 

In a further study [[3]](https://doi.org/10.48550/arXiv.2202.12565), it was found that **Akima interpolation** (bd_akima.py) returns even more accurate results. An example for corresponding interpolated curves is shown below. 


## Usage
Basic usage of this package:
```python
import numpy as np
from bd import bd_akima # can be replaced by bd_piecewise_cubic or bd_cubic

# Get test data to evaluate
# This has been measured using ffmpeg (libx265 with different preset settings).
rate1 = np.array([9487.76, 4593.60, 2486.44, 1358.24])
psnr1 = np.array([ 40.037,  38.615,  36.845,  34.851])
rate2 = np.array([9787.80, 4469.00, 2451.52, 1356.24])
psnr2 = np.array([ 40.121,  38.651,  36.970,  34.987])

bd_rate = bd_akima.bd_rate(rate1, psnr1, rate2, psnr2)
bd_psnr = bd_akima.bd_PSNR(rate1, psnr1, rate2, psnr2)
print('BD rate: ' + str("%.4f" %(bd_rate))+'%')
print('BD PSNR: ' + str("%.4f" %(bd_psnr))+' dB')
```
Other examples using the alternative interpolation methods are contained in the [example_usage.py](example_usage.py) file.


## Comparison behind the scenes
The file [example_usage.py](example_usage.py) also contains a comparison of the three variants.
The functions for BD rate computation are equipped with optional parameters, 
where axes handles can be provided to plot the interpolation curves in.

Furthermore, a comparison between the interpolated curves and intermediate, true rate-distortion points between the supporting points is shown in the plot below. 
For this example, the quality is represented by the SSIM value. Note that the example was chosen because cubic interpolation fails. Apparently, the curve interpolated by the Akima interpolator is closest to the intermediate points. 

![Measured data](doc/interpolated_curves.png)

## References
[1] G. Bjontegaard, "Calculation of average PSNR differences between RD-curves", VCEG-M33, Austin, TX, USA, April 2001. <br/>
[2] F. Bossen, " 	Common HM test conditions and software reference configurations", JCTVC-L1100, Geneva, Switzerland, April 2013. <br/>
[3] C. Herglotz, M. Kränzler, R. Mons, A. Kaup, "Beyond Bjontegaard: Limits of Video Compression Performance Comparisons", submitted to ICIP 2022, [preprint](https://doi.org/10.48550/arXiv.2202.12565) available. <br/>
