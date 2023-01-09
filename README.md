# VG-feature
A robust feature for images based on visibility graphs and Knn-filter.

Running time for a 32*32 image is approximately 40 ms

Usage:

```
import cv2
from Graph_Feature import KKFilter

I=cv2.imread('lena.png')
I=cv2.cvtColor(I,cv2.COLOR_BGR2GRAY)
VG=KKFilter(I)

plt.subplot(121)
plt.imshow(I,'gray'); plt.axis('off')
plt.subplot(122)
plt.imshow(VG,'gray'); plt.axis('off'); plt.show()
```

![plot](feature.png)




Iacovacci, Jacopo, and Lucas Lacasa. "Visibility graphs for image processing." IEEE transactions on pattern analysis and machine intelligence 42.4 (2019): 974-987.
