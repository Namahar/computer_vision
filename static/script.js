// used to check if a button has already been pressed
var buttonPressed = false;


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

function removeLoading() {
   // remove loading div
   var loading = document.getElementById('loading');
   loading.remove();

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
function removeImage() {
   var images = document.getElementsByTagName('img');

   for (let i = images.length - 1; i >= 0; i--) {
      images[i].remove();
   }

}


function contactServer(fileInput, url) {
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

      var imgData = data.substring(23, data.length);

      $.ajax({
         url: url,
         method: "POST",        
         data: imgData,
         contentType: "image/jpeg",
         timeout: 60000,
         success: function (response) {
            response = response.substring(1, response.length - 1)
            var img = 'data:image/jpeg;base64,' + response;

            removeLoading();
            showImage(img);
         }
      });
   };     
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

      const fileInput = document.getElementById('segments');
      
      showLoading()
      contactServer(fileInput, 'segments');

   });
}


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
   
      const fileInput = document.getElementById('edges');
    
      showLoading();
      contactServer(fileInput, 'edges');
   });
}