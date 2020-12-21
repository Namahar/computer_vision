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

def convolution(image, kernel):

   # get shape of image and filter
   image_row, image_col = image.shape
   kernel_row, kernel_col = kernel.shape

   output = np.zeros((image_row, image_col))

   # get padding size
   pad_height = (kernel_row - 1) // 2
   pad_width = (kernel_col - 1) // 2

   padded_image = np.zeros((image_row + 2*pad_height, image_col + 2*pad_width))

   # copy image to padded_image
   height_end = padded_image.shape[0] - pad_height
   width_end = padded_image.shape[1] - pad_width
   padded_image[pad_height:height_end, pad_width:width_end] = image

   for row in range(image_row):
      for col in range(image_col):
         row_end = row + kernel_row
         col_end = col + kernel_col
         output[row, col] = np.sum(kernel * padded_image[row:row_end, col:col_end])

   return output

def edge_detector():
   # set parameters
   sigma = 1
   width = 6*sigma + 1
   image_name = 'uploaded_file.jpg'
   
   # get grayscale image
   image = cv2.imread(image_name, 0)

   # gaussian kernel
   g = gaussian_kernel(sigma, width, False)

   # sobel edge detector
   # g = np.array([[1, 1], [2, 2], [1, 1]])
   # g_prime = np.array([[1, -1]])

   # gaussian derivative kernel
   g_prime = gaussian_kernel(sigma, width, True)

   # smoothing
   ix = convolution(image, g)
   iy = convolution(image, g.T)

   # edges
   ix_prime = convolution(ix, g_prime)
   iy_prime = convolution(iy, g_prime.T)

   # calculate magnitude
   mag = np.hypot(ix_prime, iy_prime)
   mag = (mag - np.min(mag)) / (np.max(mag) - np.min(mag))
   mag = (mag * 255).astype(np.uint8)
   cv2.imwrite('output.jpg', mag)

   return