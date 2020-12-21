from flask import Flask, render_template, request, json
import base64
from PIL import Image
from io import BytesIO
import canny
import threshold_segmentation

app = Flask(__name__)

# render html
@app.route('/')
def index():
   return render_template('index.html')


# edge detection
@app.route('/edges', methods = ['POST'])
def edge_detection():

   # receive file and save
   img = request.get_data()
   save_file(img)

   # return 'waiting'
   
   # run edge detection
   canny.edge_detector()

   # load image
   img = encode()
   
   return json.dumps(img)


@app.route('/segments', methods = ['POST'])
def image_segmentation():

   # receive file and save
   img = request.get_data()
   save_file(img)

   # run image segmentation
   threshold_segmentation.image_segmentation()

   # load image
   img = encode()

   return json.dumps(img)


# convert image to base64 to send with ajax
def encode():
   # encode image in base64 to send to client
   with open('output.jpg', 'rb') as image:
      encoding = base64.b64encode(image.read())
   encoding = encoding.decode('utf-8')

   return encoding


# save image uploaded from client
def save_file(data):
   # convert byte data back to image
   im = Image.open(BytesIO(base64.b64decode(data)))

   # save image
   im.save('uploaded_file.jpg', 'JPEG')

   return


if __name__ == '__main__':
   # run flask
   app.run(debug=True, port=8000)