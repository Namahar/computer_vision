import cv2

def otsu(histogram):
   '''
   histogram -> histogram array. index = pixel value and value at index = frequency
   returns integer for threshold
   '''
   s_max, threshold = 0, 0

   # total pixels in image for calculating class probabilities
   total_pixels = sum(histogram)

   # check every bin value for threshold calculations
   for i in range(len(histogram)):

      # class probabilities
      p1 = sum(histogram[:i])
      p2 = total_pixels - p1

      # class means
      u1 = sum([j*histogram[j]/p1 for j in range(i)]) if p1 > 0 else 0
      u2 = sum([j*histogram[j]/p2 for j in range(i+1, 256)]) if p2 > 0 else 0

      # between-class variance
      sigma = p1 * p2 * (u1-u2)**2

      # save best threshold
      if sigma > s_max:
         s_max = sigma
         threshold = i

   print('otsu threshold = ' + str(threshold))
   return threshold

def binary_thresholding(image, threshold):
   '''
   loops through image and changes pixel values to 0 or 255
   depending on if pixel value is greather or less than threshold
   image -> 2d array of pixel values
   threshold -> integer threshold
   returns binary image
   '''

   shape = image.shape
   image = image.flatten()

   for i in range(len(image)):
      image[i] = 0 if image[i] < threshold else 255

   return image.reshape(shape)

def image_segmentation():

   image_location = 'uploaded_file.jpg'

   # read image
   image = cv2.imread(image_location)

   # convert to grayscale image
   image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

   # get histogram data
   histogram = cv2.calcHist([image], [0], None, [256], [0,256])

   # ost algorithm
   threshold = otsu(histogram)

   # perform binary thresholding for segmentation
   segmentation = binary_thresholding(image, threshold)

   cv2.imwrite('output.jpg', segmentation)

   return