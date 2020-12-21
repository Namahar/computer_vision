import cv2
import numpy as np

def gaussian_kernel(sigma, width, derivative):
   half = width // 2
   x = np.mgrid[-half:half+1]

   if not derivative:
      g = np.exp(-(x**2 / (2.0*sigma**2))) / (np.sqrt(2.0*np.pi) * sigma**2)

   else:
      g = -1 * (x / sigma**2) * np.exp(-(x**2) / (2.0*sigma**2)) / (np.sqrt(2.0*np.pi) * sigma**2)

   g = g.reshape((1, g.shape[0]))

   return g

def edge_detector():
   # set parameters
   sigma = 1
   width = 6*sigma + 1
   image_name = 'uploaded_file.jpg'
   
   # get grayscale image
   image = cv2.imread(image_name, 0)

   # gaussian kernel
   g = gaussian_kernel(sigma, width, False)

   # gaussian derivative kernel
   g_prime = gaussian_kernel(sigma, width, True)

   # smoothing
   ix = cv2.filter2D(image, -1, g)
   iy = cv2.filter2D(image, -1, g.T)

   # edges
   ix_prime = cv2.filter2D(ix, -1, g_prime)
   iy_prime = cv2.filter2D(iy, -1, g_prime.T)

   # calculate magnitude
   mag = np.hypot(ix_prime, iy_prime)
   mag = (mag - np.min(mag)) / (np.max(mag) - np.min(mag))
   mag = (mag * 255).astype(np.uint8)
   cv2.imwrite('output.jpg', mag)

   return