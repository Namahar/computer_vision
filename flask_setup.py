from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
from PIL import Image
from io import BytesIO
import canny
import threshold_segmentation


app = Flask(__name__)
socketio = SocketIO(app, always_connect=True, engineio_logger=True, ping_timeout=60, ping_interval=5)


# render html
@app.route('/')
def index():
   return render_template('index.html')


# check that socket is connected
@socketio.on('connect')
def connected():
   print('connected')


# edge detection
@socketio.on('edges')
def edge_detection(data):

   save_file(data)

   # run edge detection
   print('running edge detection')
   canny.edge_detector()
   print('finished edge detection')

   image = encode()
   
   print('sending image...')
   emit('return_image', image)


# image segmentation
@socketio.on('segments')
def image_segmentation(data):
   
   save_file(data)

   # run image segmentation
   print('running image segmentation')
   threshold_segmentation.image_segmentation()
   print('finished image segmentation')

   image = encode()

   print('sending image...')
   emit('return_image', image)


# convert image to base64 to send with socket
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
   # app.run(debug=True, host='0.0.0.0', port=5000)
   
   # run socket
   socketio.run(app, debug=True)