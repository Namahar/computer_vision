// used to check if a button has already been pressed
var buttonPressed = false;


function readFile(fileInput, operation) {

   // get file   
   const image = fileInput.files[0];
   console.log('file uploaded');

   // convert image to base64
   var reader = new FileReader();
   reader.readAsDataURL(image);

   reader.onload = function() {
      var data = reader.result;

      // load original image to webpage
      showImage(data);

      // send socket
      var imgData = data.substring(23, data.length);
      if (operation == 'edges') {
         socket.emit('edges', imgData);
         console.log('edges detection starting...');
      }

      else if (operation == 'segments') {
         socket.emit('segments', imgData);
         console.log('image segmentation starting...');
      }
   }; 
}


function showLoading() {

   // add loading signal
   var imageContainer = document.getElementById('content');
   var loading = document.createElement('div');
   loading.innerText = 'loading image...';
   loading.id = 'loading';
   loading.className = 'load';
   imageContainer.appendChild(loading);

   return;
}


function showImage(data) {
   // store div to upload images too
   var imageContainer = document.getElementById('content');

   // load image to webpage
   var image = document.createElement('img');
   image.src = data;
   imageContainer.appendChild(image);
}


// remove images if another function is chosen
function removeImage(data) {
   var images = document.getElementsByTagName('img');

   for (let i = images.length - 1; i >= 0; i--) {
      images[i].remove();
   }

}


// initialize socket to send flle
var socket = io.connect('https://saeedcomputervision.herokuapp.com');
socket.on('connect', function() {
   console.log('socket init');
});


// edge detection button
const edges = document.getElementById('edges');
if (edges != null) {
   edges.addEventListener('change', function() {

      // remove images and reset boolean
      if (buttonPressed) {
         removeImage();
      }
      else {
         buttonPressed = true;
      }
      
      // var label = document.getElementById('edgeLabel');
      // label.style.backgroundColor = '#3366ff'
   
      const fileInput = document.getElementById('edges');
      readFile(fileInput, 'edges');      
      showLoading();

   });
}

// image segmentation button
const segments = document.getElementById('segments');
if (segments != null) {
   segments.addEventListener('change', function() {

      // remove images and reset boolean
      if (buttonPressed) {
         removeImage();
      }
      else {
         buttonPressed = true;
      }

      // var label = document.getElementById('segmentLabel');
      // label.style.backgroundColor = '#3366ff'

      const fileInput = document.getElementById('segments');
      readFile(fileInput, 'segments');      
      showLoading();      
   });
}


// grabs returned image from server
socket.on('return_image', function(binData) {
   console.log('file received');

   // remove loading div
   var loading = document.getElementById('loading');
   loading.remove();

   // add image
   var img = 'data:image/jpeg;base64,' + binData;
   showImage(img);

   // socket.close(1000, 'done');
});