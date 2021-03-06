from PIL import Image, ImageCms
import skimage.metrics as msr
from matplotlib import pyplot as plt
import numpy as np
from wmark import WaterMark
from pathlib import Path

path = Path(__file__).resolve()
image_path = str(path.parents[1])+'/TestSet/cmykExample.tif'
profile_path = str(path.parents[1]) + '/profiles/ISOcoated_v2_eci.icc'

# Create wmark object with seed 5
wmarkObj = WaterMark(5)

# Read and image
img = wmarkObj.imread(image_path)

# Find appropriate implementation factor to get quality (PSNR) between 20, 30 dB
factorQuality = wmarkObj.findImpactFactor(img, (20, 30))
print('for impact factor: {:.0f}, PSNR quality is: {:.2f}'.format(
    factorQuality[0], factorQuality[1]))

# Embed mark in an image
img_marked = wmarkObj.embedMark(img, factor=factorQuality[0])

# Mask wateremark using gcr masking
img_masked = wmarkObj.gcrMasking(img, img_marked, profile_path)

# Calculate and print psrn in lab
psnr_marked_lab = wmarkObj.labPSNR(img, img_marked, profile_path)
psnr_masked_lab = wmarkObj.labPSNR(img, img_masked, profile_path)

print(f'Marked Image lab >> PSNR = {psnr_marked_lab:.2f}')
print(f'Masked Image lab >> PSNR = {psnr_masked_lab:.2f}')

# Determine if the image has watermark
maxCorr = wmarkObj.decodeMark(img_masked, 'CORR')
isMarked = wmarkObj.detectOutlier(img_masked, 'CORR', alpha=0.0001)
print('Watermark is embeded: {}\nMax correlation value is {:.3f}'.format(
    isMarked, maxCorr))

# Show images
WaterMark.compareImages(img, img_marked, img_masked, profile_path)
