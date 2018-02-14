from skimage import data
from skimage import filters
from skimage import img_as_float
from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np

unsharp_strength = 0.9
blur_size =   10 # Standard deviation in pixels.

# Convert to float so that negatives don't cause problems
image = imread("./Selection_206.png",as_grey=True)
LPF_image = filters.median(image)

# highpass = image - unsharp_strength * blurred
# sharp = image + highpass


fig=plt.figure()
ax=fig.add_subplot(211)
ax.imshow(LPF_image, vmin=0, vmax=1)
ax=fig.add_subplot(212)
ax.imshow(image, vmin=0, vmax=1)

plt.show()