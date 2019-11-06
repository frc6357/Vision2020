from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt
import numpy as np

lower_bound = (38, 255, 212)
upper_bound = (38, 255, 235)
target_color = (82, 255, 212.7975)
lo_square = np.full((10, 10, 3), lower_bound, dtype=np.uint8) / 255.0
up_square = np.full((10, 10, 3), upper_bound, dtype=np.uint8) / 255.0
co_square = np.full((10, 10, 3), target_color, dtype=np.uint8) / 255.0
plt.subplot(1, 3, 1)
plt.imshow(hsv_to_rgb(up_square))
plt.subplot(1, 3, 2)
plt.imshow(hsv_to_rgb(lo_square))
plt.subplot(1, 3, 3)
plt.imshow(hsv_to_rgb(co_square))
plt.show()
